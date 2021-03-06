import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_albums(data, x_, y_, hue_, start_date, end_date):
        
        df = pd.DataFrame(data)
        df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d').dt.year
        
        df = df.groupby('album_name').agg({x_:'mean', y_: 'mean', 'duration_ms': 'sum', 'artist_name': 'first', 'release_date': 'first'}).reset_index()
        df['duration_ms'] = pd.to_datetime(df['duration_ms'], unit='ms')
        df['duration_ms'] = pd.to_datetime(df['duration_ms'], format= '%H:%M:%S').dt.time
        df = df.sort_values(['release_date'], ascending=[True])
        if start_date != None and end_date != None:
                df = df.loc[(df['release_date'] >= start_date) & (df['release_date'] <= end_date)]
        print(df)

        plt.figure(figsize=(12,8))
        ax = sns.scatterplot(data=df, x=x_, y=y_, 
                            hue=hue_, palette='muted', 
                            size='duration_ms', sizes=(100,2000), 
                            alpha=.7)
        
        handles,labels = ax.get_legend_handles_labels()
        n_albums = len(df.index)
        ax.legend(handles[1:20], labels[1:n_albums+1], loc='center left',
                bbox_to_anchor=(1, 0.5),
                title=None,
                frameon=False)
        plt.subplots_adjust(right=0.65)
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.show()