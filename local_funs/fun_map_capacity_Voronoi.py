

import pandas as pd
#import geopandas as gpd

def fun_map_capacity_Voronoi(carrier, token_density, n, ax):
    """
    This function plots the installed capacity of a generator carrier in Voronoi cells
    """

    ##### Get df with capacity
    gg = n.generators
    # filter carrier
    df = gg[gg['carrier']==carrier]
    # remove zero_capacities
    df = df.loc[ df['p_nom']>0 , ['carrier', 'bus', 'p_nom']]


    ##### Get gdf with geometry and area
    if 'off' in carrier:
        gdf = n.shapes[ (n.shapes['type']=='offshore') & (n.shapes['component']=='Bus')].copy()
    else:
        gdf = n.shapes[ (n.shapes['type']=='onshore') & (n.shapes['component']=='Bus')].copy()

    gdf.rename(columns={'idx': 'bus'}, inplace=True)

    gdf = gdf[['geometry', 'bus']]

    # Add area [km2]
    gdf_area = gdf.to_crs(3035)
    gdf['area'] = gdf_area.area/1e6

 
    ##### Merge and add capacity density
    gdf_merged =  pd.merge(gdf,df, on='bus')
    gdf_merged['p_nom_density'] = gdf_merged['p_nom'] / gdf_merged['area']



    ##### Plot in map

    if token_density == 0:
        gdf_merged.plot(ax=ax, column='p_nom', cmap='viridis', edgecolor="black", legend=True, alpha=1)
        total_capacity = gdf_merged['p_nom'].sum()
        ax.set_title(f'{carrier} : Installed capacity [MW]. Total: {total_capacity:.2f}')

    if token_density == 1:
        gdf_merged.plot(ax=ax, column='p_nom_density', cmap='viridis', edgecolor="black", legend=True, alpha=1)
        ax.set_title(f'{carrier} : Installed capacity density [MW/km2]')


