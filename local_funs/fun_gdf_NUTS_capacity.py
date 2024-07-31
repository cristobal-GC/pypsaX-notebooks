########## Get gdf at NUTS level

import pandas as pd
import geopandas as gpd

from fun_gdf_network_capacity import fun_gdf_network_capacity


def fun_gdf_NUTS_capacity(carrier, n, gdf_NUTS):
    """
    This function provides a gdf of a network with some generation capacity features 
    aggregated at NUTS level for a specific carrier.

    Columns:
      - NUTS_ID
      - geometry
      - area
      - carrier
      - weighted_p_nom               : installed capacity [MW]
      - weighted_p_nom_density       : ratio between p_nom and area [MW/km2]
      - weighted_p_nom_max           : potential according to land availability [MW]
      - weighted_p_nom_max_density   : ratio between p_nom_max and area [MW/km2]
      - weighted_p_nom_max_ratio     : ration between p_nom and p_nom_max [-]

    The gdf is provided in Plate Carrée crs('4036')    
    """

    gdf_network_capacity = fun_gdf_network_capacity(carrier, n)
    gdf_network_capacity = gdf_network_capacity.to_crs('3035')


    ##### gdf_NUTS, retain relevant columns and add area
    gdf_NUTS = gdf_NUTS[['NUTS_ID', 'geometry']]
    # Put in crs (3035)
    gdf_NUTS = gdf_NUTS.to_crs(3035)
    # Add area_NUTS [km2]
    gdf_NUTS['area_NUTS'] = gdf_NUTS.area/1e6


    ##### Make intersection, and group by NUTS
    intersected = gpd.overlay(gdf_network_capacity, gdf_NUTS, how='intersection')
    # Get intersected area
    intersected['area_intersection'] = intersected.geometry.area
    # Get weighted p_nom according to percentage of intersected areas
    intersected['weighted_p_nom'] = intersected['p_nom'] * (intersected['area_intersection'] / intersected['area']/1e6) # 'area' refers to Voronoi cell
    intersected['weighted_p_nom_max'] = intersected['p_nom_max'] * (intersected['area_intersection'] / intersected['area']/1e6) # 'area' refers to Voronoi cell


    df_p_nom = intersected.groupby('NUTS_ID')['weighted_p_nom'].sum().reset_index()
    df_p_nom_max = intersected.groupby('NUTS_ID')['weighted_p_nom_max'].sum().reset_index()


    ##### Merge gdf_NUTS and p_nom_by_NUTS, gdf_NUTS_capacity
    gdf_NUTS_capacity = pd.merge(gdf_NUTS, df_p_nom, on='NUTS_ID')
    gdf_NUTS_capacity = pd.merge(gdf_NUTS_capacity, df_p_nom_max, on='NUTS_ID')
    gdf_NUTS_capacity['weighted_p_nom_density'] = gdf_NUTS_capacity['weighted_p_nom'] / gdf_NUTS_capacity['area_NUTS']
    gdf_NUTS_capacity['weighted_p_nom_max_density'] = gdf_NUTS_capacity['weighted_p_nom_max'] / gdf_NUTS_capacity['area_NUTS']
    gdf_NUTS_capacity['weighted_p_nom_max_ratio'] = gdf_NUTS_capacity['weighted_p_nom'] / gdf_NUTS_capacity['weighted_p_nom_max']
    
    gdf_NUTS_capacity = gdf_NUTS_capacity.to_crs('4036')



    return gdf_NUTS_capacity


