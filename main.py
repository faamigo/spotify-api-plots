import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from credentials import CLIENT_ID, CLIENT_SECRET

class Spotify:

    def __init__(self):

        self.auth_url = "https://accounts.spotify.com/api/token"
        self.base_url = "https://api.spotify.com/v1/"
        self.access_token = ''
        self.headers = {}
    
    def authentication(self, client_id, client_secret):

        auth_response = requests.post(self.auth_url, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        })

        if auth_response.status_code == 200:
            res = "authenticated"
            auth_response_data = auth_response.json()
            self.access_token = auth_response_data['access_token']
            self.headers = {
                'Authorization': 'Bearer {token}'.format(token=self.access_token)
            }
            return res      

        else:
            res = "authentication error"
            print(res)
            return res
            

    def plot_all_artist_albums(self, artist_id, x_, y_, hue_):

        res_albums = requests.get(self.base_url + 'artists/' + artist_id + '/albums', 
                        headers=self.headers, 
                        params={'include_groups': 'album','limit': 50})
        artist_albums = res_albums.json()
        
        # GET all albums ids
        albums_ids = {}
        for album in artist_albums['items']:
            standarized_name = album['name'].split('(')[0].upper().strip()
            if  standarized_name not in albums_ids.values():
                albums_ids[album['id']] = standarized_name
        
        # GET multiple albums
        n_albums = len(albums_ids)
        all_albums_list = []
        for i in range(0, n_albums, 20):
            all_albums_list.append(dict(list(albums_ids.items())[i:i+20]))
        
        all_albums = []
        for albums_group in all_albums_list:
            res_mult_albums = requests.get(self.base_url + 'albums?ids=' + ','.join(albums_group), headers=self.headers)
            all_albums.extend(res_mult_albums.json()['albums'])
        
        
        # GET all tracks info
        all_tracks = {}
        for album in all_albums:
            for track in album['tracks']['items']:
                all_tracks[track['id']] = {'track_number': track['track_number'], 'name': track['name'],
                                           'album_name': album['name'], 'release_date': album['release_date']}

        # Adding audio features to track info
        n_tracks = len(all_tracks)
        all_tracks_list = []
        for i in range(0, n_tracks, 100):
            all_tracks_list.append(dict(list(all_tracks.items())[i:i+100]))

        
        tracks_features = []
        all_ids = ''
        
        for tracks_group in all_tracks_list:
            all_group_ids = ','.join(tracks_group)
            if all_ids == '':
                all_ids += all_group_ids
            else:
                all_ids += ',' + all_group_ids
            res_mult_tracks = requests.get(self.base_url + 'audio-features?ids=' + all_group_ids, headers=self.headers)
            tracks_features.extend(res_mult_tracks.json()['audio_features'])
        
        k = 0
        for id_ in all_ids.split(','):
            tracks_features[k]['track_number'] = all_tracks[id_]['track_number']
            tracks_features[k]['name'] = all_tracks[id_]['name']
            tracks_features[k]['album_name'] = all_tracks[id_]['album_name']
            tracks_features[k]['release_date'] = all_tracks[id_]['release_date']
            k += 1
        
        # Plot settings
        df = pd.DataFrame(tracks_features)
        df['release_date'] = pd.to_datetime(df['release_date'])
        df = df.sort_values(['release_date', 'album_name', 'track_number'], ascending=[True, True, True])
        
        aggregate = df.groupby('album_name').agg({x_:'mean', y_: 'mean', 'duration_ms': 'sum'}).reset_index()
        aggregate['duration_ms'] = pd.to_datetime(aggregate['duration_ms'], unit='ms')
        aggregate['duration_ms'] = pd.to_datetime(aggregate['duration_ms'], format= '%H:%M:%S').dt.time
        print(aggregate)

        plt.figure(figsize=(12,8))
        ax = sns.scatterplot(data=aggregate, x=x_, y=y_, 
                            hue=hue_, palette='muted', 
                            size='duration_ms', sizes=(100,2000), 
                            alpha=.7)
        
        handles,labels = ax.get_legend_handles_labels()
        ax.legend(handles[1:10], labels[1:n_albums+1], loc='center left',
                bbox_to_anchor=(1, 0.5),
                title=None,
                frameon=False)
        plt.subplots_adjust(right=0.65)
        plt.show()


    def search_artist(self):

        query = input("Search artist: ")
        res = requests.get(self.base_url + 'search?q=' + query + '&type=artist', headers=self.headers)
        artists = res.json()['artists']['items']

        artists_id = {}
        for artist in artists:
            artists_id[artist['name']] = {'id': artist['id'], 'genres': artist['genres']}

        return artists_id
        
        

if __name__ == '__main__':

    spotify_api = Spotify()
    res = spotify_api.authentication(CLIENT_ID, CLIENT_SECRET)    

    if res == 'authenticated':
        response = spotify_api.search_artist()
        if response != None:
            for res in response:
                print(response[res]['id'], res, response[res]['genres'])
            
            artist_id = input("Enter artist id: ")
            spotify_api.plot_all_artist_albums(artist_id, 'danceability', 'valence', 'album_name')
