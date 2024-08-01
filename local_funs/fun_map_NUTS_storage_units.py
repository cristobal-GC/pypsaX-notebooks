

#import pandas as pd
#import geopandas as gpd

from fun_gdf_NUTS_storage_units import fun_gdf_NUTS_storage_units



def fun_map_NUTS_storage_units(carrier, n, gdf_NUTS, feature, ax):
    """
    This function plots a storage unit capacity related feature
    of a storage unit carrier aggregated to NUTS level.

    Features:
      - area_NUTS
      - weighted_p_nom               : installed capacity [MW]
      - weighted_p_nom_density       : ratio between p_nom and area [MW/km2]
    """

    gdf_NUTS_storage_units = fun_gdf_NUTS_storage_units(carrier, n, gdf_NUTS)



    ##### Plot in map


    gdf_NUTS_storage_units.plot(ax=ax, column=feature, cmap='viridis', edgecolor="black", legend=True, alpha=1)


    if feature=='area_NUTS':
        total = gdf_NUTS_storage_units[feature].sum()
        ax.set_title(f'Area. Total: {total:.2f} km2')

    if feature=='weighted_p_nom':
        total = gdf_NUTS_storage_units[feature].sum()
        ax.set_title(f'{carrier} : Installed capacity. Total: {total:.2f} MW')        

    if feature=='weighted_p_nom_density':
        ax.set_title(f'{carrier} : Installed capacity density [MW/km2]')

           


