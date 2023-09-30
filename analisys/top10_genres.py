import ast
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def top10_genres(dataframe):
    """
    This function takes a pandas dataframe as input and generates a bar chart of the top 10 genres based on the number of tracks in the dataframe.
    
    Parameters:
    dataframe (pandas.DataFrame): The input dataframe containing the track information.
    
    Returns:
    None
    """
    # Create a copy of the input dataframe
    df = dataframe.copy()

    # Convert the 'genres' column from string to list of strings
    df['genres'] = df['genres'].apply(ast.literal_eval)
    # Extract the first genre from the list of genres and create a new column 'main_genre'
    df['main_genre'] = df['genres'].apply(lambda x: x[0] if x else None)
    # Count the number of tracks for each genre
    genre_counts = df['main_genre'].value_counts()

    # plot the bar chart
    plt.style.use('dark_background')
    # Define the color palette for the bar chart
    palette = sns.color_palette('RdPu', 10)[::-1]
    sns.set_palette(palette)
    sns.color_palette("rocket")
    # Create a figure with size 12x6 inches
    plt.figure(figsize=(12, 6))
    # Set the title of the plot
    plt.title('Top 10 Genres')
    # Create a horizontal bar plot with the top 10 genres and their counts
    barplot = sns.barplot(y=genre_counts[:10].index, x=genre_counts[:10].values, orient='h')
    # Set the x and y axis labels
    plt.xlabel('Number of tracks', fontsize=14, fontweight='bold')
    plt.ylabel('Genre', fontsize=14, fontweight='bold')
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
    plt.savefig('top10_genres.png')
    # Show the plot
    plt.show()
