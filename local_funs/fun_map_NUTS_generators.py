

#import pandas as pd
#import geopandas as gpd

from fun_gdf_NUTS_generators import fun_gdf_NUTS_generators



def fun_map_NUTS_generators(carrier, n, gdf_NUTS, feature, ax):
    """
    This function plots a generation capacity related feature
    of a generator carrier aggregated to NUTS level.

    Features:
      - area_NUTS
      - weighted_p_nom               : installed capacity [MW]
      - weighted_p_nom_density       : ratio between p_nom and area [MW/km2]
      - weighted_p_nom_max           : potential according to land availability [MW]
      - weighted_p_nom_max_density   : ratio between p_nom_max and area [MW/km2]
      - weighted_p_nom_max_ratio     : ration between p_nom and p_nom_max [-]
    """

    gdf_NUTS_generators = fun_gdf_NUTS_generators(carrier, n, gdf_NUTS)



    ##### Plot in map


    gdf_NUTS_generators.plot(ax=ax, column=feature, cmap='viridis', edgecolor="black", legend=True, alpha=1)


    if feature=='area_NUTS':
        total = gdf_NUTS_generators[feature].sum()
        ax.set_title(f'Area. Total: {total:.2f} km2')

    if feature=='weighted_p_nom':
        total = gdf_NUTS_generators[feature].sum()
        ax.set_title(f'{carrier} : Installed capacity. Total: {total:.2f} MW')        

    if feature=='weighted_p_nom_density':
        ax.set_title(f'{carrier} : Installed capacity density [MW/km2]')

    if feature=='weighted_p_nom_max':
        total = gdf_NUTS_generators[feature].sum()
        ax.set_title(f'{carrier} : Potential. Total: {total:.2f} MW')    

    if feature=='weighted_p_nom_max_density':
        ax.set_title(f'{carrier} : Potential density [MW/km2]')                    

    if feature=='weighted_p_nom_max_ratio':
        total = gdf_NUTS_generators[feature].sum()
        ax.set_title(f'{carrier} : ratio installed capacity / potential')                


