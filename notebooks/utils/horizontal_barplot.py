import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def horizontal_barplot(x, y, title, xlabel, ylabel, filename, total_entries):
    # plot most active users by number of tracks added
    # color palette
    plt.style.use("dark_background")
    palette = sns.color_palette("RdPu", 10)[::-1]
    sns.set_palette(palette)
    sns.color_palette("rocket")

    # create a figure with size 12x6
    plt.figure(figsize=(12, 6))

    # set labels and titles
    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel(xlabel, fontsize=14, fontweight="bold")
    plt.ylabel(ylabel, fontsize=14, fontweight="bold")

    # Create a horizontal bar plot 
    barplot = sns.barplot(
            x=x,
            y=y,
            palette=palette,
            edgecolor="black",
            orient="h",
    )

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
            

    # Add total of tracks as side information on the graph

    total_tracks = total_entries
    plt.text(
            x = 0.98, 
            y = 0.02, 
            s = f'Total tracks: {total_tracks}', 
            transform=plt.gca().transAxes, 
            fontsize=12, 
            horizontalalignment='right'
            )


    # adjust the layout of the plot
    plt.tight_layout()

    # save the plot as a png file
    plt.savefig(f"../images/f{filename}", dpi=300)

    plt.show()