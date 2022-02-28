import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
from matplotlib.font_manager import FontProperties

# For testing purposes in PyCharm
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def draw_plot():
    # Set default fonts
    plt.rcParams['font.family'] = 'fantasy'
    plt.rcParams['font.fantasy'] = ['Impact']

    # Set background colour
    plt.rcParams['axes.facecolor'] = 'lightsteelblue'

    # Set style
    plt.style.use('Solarize_Light2')

    # Import data of min wages 2016-2021
    df = pd.read_csv('russian_flights_banned.csv', encoding='latin1')

    # Load base map
    world = gpd.read_file('ne_10m_admin_0_countries')

    # Set better projection
    world = world.to_crs(epsg=3035)

    # Filter for Europe
    world = world[(world['CONTINENT'] == 'Europe') | (world['NAME'] == 'Turkey')]

    # Plot base map
    base = world.plot(color='dimgray', figsize=(16,9), edgecolor='black',linewidth=.2)

    # Merge the map and data
    table = world.merge(df, right_on='country', left_on='NAME')

    # Import data that shows coordinates of centres of all countries
    countrycentre=pd.read_csv('countriescentre.csv', encoding='latin1')

    # Merge DataFrames to show ban info of countries in Europe
    centre_with_banned_info = df.merge(countrycentre)

    # Create geopandas DataFrame
    centre_with_banned_info_gdf = gpd.GeoDataFrame(centre_with_banned_info, crs=4326,
                        geometry=gpd.points_from_xy(x=centre_with_banned_info.longitude,
                                                     y=centre_with_banned_info.latitude))
    print('centre with banned info gdb: \n', centre_with_banned_info_gdf)

    # Suit projection to base map
    centre_with_banned_info_gdf = centre_with_banned_info_gdf.to_crs(epsg=3035)

    # Plot ready map
    table.plot(ax=base, edgecolor='black', linewidth=.4, legend=True, column='status', cmap='Spectral')

    fp = FontProperties(fname=r"Font Awesome 6 Free-Solid-900.otf")

    # Annotating minimum wages over each countries
    for idx, row in centre_with_banned_info_gdf.iterrows():
        if row['status'] == 'banned':
            txt = plt.text(x=row.geometry.x, y=row.geometry.y, s="\ue069", fontproperties=fp,
                            color='white', family='arial', wrap=True,
                           horizontalalignment='center', verticalalignment='center')

        # Set black border color of each characters for better readability
            txt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])

    # Add title to the plot
    title = plt.text(x=4.3*1e6, y=4.3*1e6, s='Countries banned Russian flights',
                     fontsize=28, color='white', horizontalalignment='center', verticalalignment='center')

    # Set black border color of each characters for better readability
    title.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])

    # Remove axes
    plt.xticks([])
    plt.yticks([])
    
    # Zoom the area of Europe
    bounds = centre_with_banned_info_gdf.geometry.bounds
    plt.xlim([bounds.minx.min()-0.5*1e6, bounds.maxx.max()+0.3*1e6])
    plt.ylim([bounds.miny.min()-0.5*1e6, bounds.maxy.max()+0.7*1e6])

    # Plot the map
    plt.tight_layout()
    plt.show()

draw_plot()
