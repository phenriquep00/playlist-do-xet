from ast import literal_eval
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def top10_artists(dataframe):
    df = dataframe.copy()

    # Convert the string representation of list to actual list
    df['track_artists'] = df['track_artists'].apply(literal_eval)

    # Explode the dataframe on 'track_artists' column, so we have one row per artist per track
    df_exploded = df.explode('track_artists')

    # Count the number of tracks for each artist
    artist_counts = df_exploded['track_artists'].value_counts()

    # plot the bar chart
    plt.style.use('dark_background')
    # Define the color palette for the bar chart
    palette = sns.color_palette('RdPu', 10)[::-1]
    sns.set_palette(palette)
    sns.color_palette("rocket")
    # Create a figure with size 12x6 inches
    plt.figure(figsize=(12, 6))
    # Set the title of the plot
    plt.title('Top 10 Artists by number of tracks')
    # Create a horizontal bar plot with the top 10 artists and their counts
    barplot = sns.barplot(y=artist_counts[:10].index, x=artist_counts[:10].values, orient='h')
    # Set the x and y axis labels
    plt.xlabel('Number of tracks', fontsize=14, fontweight='bold')
    plt.ylabel('Artist', fontsize=14, fontweight='bold')
    # Add the total number of tracks inside the bars
    for i, p in enumerate(barplot.patches):
        width = p.get_width()
        # Get the RGB color of the bar and convert it to HSV
        rgb_color = mcolors.colorConverter.to_rgb(palette[i])
        hsv_color = mcolors.rgb_to_hsv(rgb_color)
        # If the value/brightness component of the HSV color is less than 0.5, set the text color to white, else set it to black
        text_color = 'white' if hsv_color[2] < 0.5 else 'black'
        # Add the text inside the bar
        plt.text(x = width/2,
                y = p.get_y()+(p.get_height()/2), 
                s = '{:.0f}'.format(width),
                va = 'center',
                color = text_color,  # Set the text color
                fontsize = 14,
                fontweight = 'bold')
        
    # Add total tracks as side information on the graph
    total_tracks = df['track_id'].nunique()
    plt.text(x = 0.98, y = 0.02, s = f'Total tracks: {total_tracks}', transform=plt.gca().transAxes, fontsize=12, horizontalalignment='right')

    # Adjust the layout of the plot
    plt.tight_layout()
    # Save the plot as a PNG file
    plt.savefig('top10_artists.png')
    plt.show()

