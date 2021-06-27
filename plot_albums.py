import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_albums(data, x_, y_, hue_, n):
        
        df = pd.DataFrame(data)
        df['release_date'] = pd.to_datetime(df['release_date'])
        df = df.sort_values(['release_date', 'album_name', 'track_number'], ascending=[True, True, True])
        
        aggregate = df.groupby('album_name').agg({x_:'mean', y_: 'mean', 'duration_ms': 'sum', 'artist_name': 'first'}).reset_index()
        aggregate['duration_ms'] = pd.to_datetime(aggregate['duration_ms'], unit='ms')
        aggregate['duration_ms'] = pd.to_datetime(aggregate['duration_ms'], format= '%H:%M:%S').dt.time
        print(aggregate)

        plt.figure(figsize=(12,8))
        ax = sns.scatterplot(data=aggregate, x=x_, y=y_, 
                            hue=hue_, palette='muted', 
                            size='duration_ms', sizes=(100,2000), 
                            alpha=.7)
        
        handles,labels = ax.get_legend_handles_labels()
        ax.legend(handles[1:20], labels[1:n+1], loc='center left',
                bbox_to_anchor=(1, 0.5),
                title=None,
                frameon=False)
        plt.subplots_adjust(right=0.65)
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.show()