

#import pandas as pd
#import geopandas as gpd

from fun_gdf_network_capacity import fun_gdf_network_capacity



def fun_map_network_capacity(carrier, n, feature, ax):
    """
    This function plots a generation capacity related feature
    of a generator carrier in Voronoi cells.

    Features:
      - area
      - p_nom               : installed capacity [MW]
      - p_nom_density       : ratio between p_nom and area [MW/km2]
      - p_nom_max           : potential according to land availability [MW]
      - p_nom_max_density   : ratio between p_nom_max and area [MW/km2]
      - p_nom_max_ratio     : ration between p_nom and p_nom_max [-]
    """

    gdf_network_capacity = fun_gdf_network_capacity(carrier, n)



    ##### Plot in map


    gdf_network_capacity.plot(ax=ax, column=feature, cmap='viridis', edgecolor="black", legend=True, alpha=1)


    if feature=='area':
        total = gdf_network_capacity[feature].sum()
        ax.set_title(f'Area. Total: {total:.2f} km2')

    if feature=='p_nom':
        total = gdf_network_capacity[feature].sum()
        ax.set_title(f'{carrier} : Installed capacity. Total: {total:.2f} MW')        

    if feature=='p_nom_density':
        ax.set_title(f'{carrier} : Installed capacity density [MW/km2]')

    if feature=='p_nom_max':
        total = gdf_network_capacity[feature].sum()
        ax.set_title(f'{carrier} : Potential. Total: {total:.2f} MW')    

    if feature=='p_nom_max_density':
        ax.set_title(f'{carrier} : Potential density [MW/km2]')                    

    if feature=='p_nom_max_ratio':
        total = gdf_network_capacity[feature].sum()
        ax.set_title(f'{carrier} : ratio installed capacity / potential')                


