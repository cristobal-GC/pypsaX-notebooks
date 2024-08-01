



#import pandas as pd
#import geopandas as gpd

from fun_gdf_NUTS_loads import fun_gdf_NUTS_loads



def fun_map_NUTS_loads(n, gdf_NUTS, feature, ax):
    """
    This function plots load features aggregated to NUTS level.

    Features:
      - area_NUTS
      - weighted_annual_load         : [TWh]
      - weighted_annual_load_density : [GWh/km2]
    """

    gdf_NUTS_loads = fun_gdf_NUTS_loads(n, gdf_NUTS)



    ##### Plot in map


    gdf_NUTS_loads.plot(ax=ax, column=feature, cmap='viridis', edgecolor="black", legend=True, alpha=1)


    if feature=='area_NUTS':
        total = gdf_NUTS_loads[feature].sum()
        ax.set_title(f'Area. Total: {total:.2f} km2')

    if feature=='weighted_annual_load':
        total = gdf_NUTS_loads[feature].sum()
        ax.set_title(f'Annual load. Total: {total:.2f} TWh')        

    if feature=='weighted_annual_load_density':
        ax.set_title(f'Annual load density [GWh/km2]')



