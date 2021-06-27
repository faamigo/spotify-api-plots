# Analysing tracks audio-features using Spotify API
## Plotting Audio Features

This program plots audio features for all tracks of one or two artists simultaneously.

### Parameters:
```artist_id```, ```artist_id_1``` and ```artist_id_2``` : Artists ids.
```x_``` : x-axis audio feature.
```y_``` : y-axis audio feature.
```hue_``` : Hue grouping attribute.
### Available methods:

- ```search_artist(self)  ``` : Will ask you on console to search an artist. Return an array with all results on the following format:  ```[artist_id] [artist_name] [artist_genres]```.

- ```plot_two_artists_albums(self, artist_1_id, artist_2_id, x_, y_, hue_)``` : Plot all albums of two bands simultaneously

- ```plot_artist_albums(self, artist_id, x_, y_, hue_)``` : Plot all albums of one band.

### Hue grouping attributes available:
- ```artist_name```
- ```album_name```
- ```release_date```

### Audio features available:
- ```acousticness```: A confidence measure of whether the track is acoustic. (0.0 - 1.0)
- ```danceability``` : Value represents whether the track is less or more danceable. (0.0 - 1.0)
- ```energy```: Represents a perceptual measure of intensity and activity. (0.0 - 1.0)
- ```instrumentalness``` : Values above 0.5 are intended to represent instrumental tracks.
- ```key``` : Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
- ```liveness``` : A value above 0.8 provides strong likelihood that the track is live.
- ```loudness``` : Values typical range between -60 and 0 db.
- ```mode``` : Major is represented by 1 and minor is 0.
- ```speechiness``` : The more exclusively speech-like the recording, the closer to 1.0 the attribute value.
- ```tempo``` : The overall estimated tempo of a track in beats per minute (BPM).
- ```time_signature``` : An estimated overall time signature. Specify how many beats are in each bar (or measure).
- ```valence``` : A measure describing the musical positiveness conveyed by a track. (0.0 - 1.0).
