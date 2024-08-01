########## Get gdf at NUTS level

import pandas as pd
import geopandas as gpd

from fun_gdf_network_loads import fun_gdf_network_loads


def fun_gdf_NUTS_loads(n, gdf_NUTS):
    """
    This function provides a gdf of a network with some load features 
    aggregated at NUTS level.

    Columns:
      - NUTS_ID
      - geometry
      - area_NUTS                       : [km2]
      - weighted_annual_load            : [TWh]
      - weighted_annual_load_density    : [GWh/km2] 

    The gdf is provided in Plate Carrée crs('4036')    
    """

    gdf_network_loads = fun_gdf_network_loads(n)
    gdf_network_loads = gdf_network_loads.to_crs('3035')


    ##### gdf_NUTS, retain relevant columns and add area
    gdf_NUTS = gdf_NUTS[['NUTS_ID', 'geometry']]
    # Put in crs (3035)
    gdf_NUTS = gdf_NUTS.to_crs(3035)
    # Add area_NUTS [km2]
    gdf_NUTS['area_NUTS'] = gdf_NUTS.area/1e6


    ##### Make intersection, and group by NUTS
    intersected = gpd.overlay(gdf_network_loads, gdf_NUTS, how='intersection')
    # Get intersected area
    intersected['area_intersection'] = intersected.geometry.area
    # Get weighted p_nom according to percentage of intersected areas
    intersected['weighted_annual_load'] = intersected['annual_load'] * (intersected['area_intersection'] / intersected['area']/1e6) # 'area' refers to Voronoi cell


    df_annual_load = intersected.groupby('NUTS_ID')['weighted_annual_load'].sum().reset_index()


    ##### Merge gdf_NUTS and df_annual_load
    gdf_NUTS_loads = pd.merge(gdf_NUTS, df_annual_load, on='NUTS_ID')
    # Add more columns
    gdf_NUTS_loads['weighted_annual_load_density'] = gdf_NUTS_loads['weighted_annual_load'] / gdf_NUTS_loads['area_NUTS']
    # Put in GWh/km2
    gdf_NUTS_loads['weighted_annual_load_density'] = gdf_NUTS_loads['weighted_annual_load_density']*1e3

    gdf_NUTS_loads = gdf_NUTS_loads.to_crs('4036')



    return gdf_NUTS_loads


