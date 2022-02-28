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
    print('this is df: \n', df)
    #
    # # Clean the data
    # df.drop(['Flag and Footnotes'], axis=1, inplace=True)
    # df.drop(df[df['banned'] == 'no'].index, inplace=True)
    # df.replace(to_replace="Germany (until 1990 former territory of the FRG)", value="Germany", inplace=True)
    # df.replace(to_replace=':', value='NaN', inplace=True)
    # df.sort_values('GEO', inplace=True)
    # df.rename(columns={'GEO':'name'}, inplace=True)
    # df['Value']=df['Value'].astype(float)
    # df['Value']=df['Value'].round()
    # df.dropna(axis=0, how='any', inplace=True)
    # df['Value']=df['Value'].apply(lambda x: int(x))
    #
    # # Show only second half of 2020
    # df.drop(df[df['TIME'] != '2020S2'].index, inplace=True)

    # Load base map
    world = gpd.read_file('ne_10m_admin_0_countries')
    print('world geodb: \n', world)
    # Customize column names for merging with DataFrame
    world.rename(columns={'name':'country_name'}, inplace=True)

    # Set better projection
    world = world.to_crs(epsg=3035)

    # Filter for Europe
    world = world[(world['CONTINENT'] == 'Europe') | (world['NAME'] == 'Turkey')]

    # Plot base map
    base = world.plot(color='dimgray', figsize=(16,9), edgecolor='black',linewidth=.2)

    # Merge the map and data
    table = world.merge(df, right_on='country', left_on='NAME')
    # print(table)
    # Import data that shows coordinates of centres of all countries
    countrycentre=pd.read_csv('countriescentre.csv', encoding='latin1')
    #print('countryCentre file: \n',countrycentre)

    # # Customize for merging
    # countrycentre.replace(to_replace='Czech Republic', value='Czechia', inplace=True)

    # Merge DataFrames to show minimum wages and coordinates of countries in Europe
    centre_with_banned_info = df.merge(countrycentre)
    #print('centre with banned info \n', centre_with_banned_info)
    #
    # Create geopandas DataFrame
    centre_with_banned_info_gdf = gpd.GeoDataFrame(centre_with_banned_info, crs=4326,
                        geometry=gpd.points_from_xy(x=centre_with_banned_info.longitude,
                                                     y=centre_with_banned_info.latitude))
    print('centre with banned info gdb: \n', centre_with_banned_info_gdf)
    # Suit projection to base map
    centre_with_banned_info_gdf = centre_with_banned_info_gdf.to_crs(epsg=3035)

    # Optional markers on map indicates countries:
    centre_with_banned_info_gdf.plot(marker='.', markersize=3 ,color='red', ax=base)

    # Plot ready map
    table.plot(ax=base, edgecolor='black', linewidth=.4, legend=True, column='status', cmap='Spectral', #vmax=2000, vmin= 300,
              # Customize appearance of legend

                legend_kwds={'fontsize': 15}

              #  legend_kwds={'location': 'bottom', 'spacing': 'proportional',
              #               'shrink': .50, 'pad': -0.09,
              #               'aspect': 50}
               )

    fp = FontProperties(fname=r"Font Awesome 6 Free-Solid-900.otf")

    # Annotating minimum wages over each countries
    for idx, row in centre_with_banned_info_gdf.iterrows():
        if row['status'] == 'banned':
            txt = plt.text(x=row.geometry.x, y=row.geometry.y, s="\ue069", fontproperties=fp,
                            color='white', # fontsize=(row['Value'] ** 0.35),
                           family='arial', # rotation=row['longitude']/4,
                           wrap=True, # fontproperties={'weight':1000, 'variant':'small-caps'},
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
    #
    # Zoom the area of Europe
    bounds = centre_with_banned_info_gdf.geometry.bounds
    plt.xlim([bounds.minx.min()-0.5*1e6, bounds.maxx.max()+0.3*1e6])
    plt.ylim([bounds.miny.min()-0.5*1e6, bounds.maxy.max()+0.7*1e6])

    # Plot the map
    plt.tight_layout()
    plt.show()

draw_plot()
