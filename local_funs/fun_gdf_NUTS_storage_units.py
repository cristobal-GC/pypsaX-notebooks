########## Get gdf at NUTS level

import pandas as pd
import geopandas as gpd

from fun_gdf_network_storage_units import fun_gdf_network_storage_units


def fun_gdf_NUTS_storage_units(carrier, n, gdf_NUTS):
    """
    This function provides a gdf of a network with some storage units capacity features 
    aggregated at NUTS level for a specific carrier.

    Columns:
      - NUTS_ID
      - geometry
      - area
      - carrier
      - weighted_p_nom               : installed capacity [MW]
      - weighted_p_nom_density       : ratio between p_nom and area [MW/km2]

    The gdf is provided in Plate Carrée crs('4036')    
    """

    gdf_network_storage_units = fun_gdf_network_storage_units(carrier, n)
    gdf_network_storage_units = gdf_network_storage_units.to_crs('3035')


    ##### gdf_NUTS, retain relevant columns and add area
    gdf_NUTS = gdf_NUTS[['NUTS_ID', 'geometry']]
    # Put in crs (3035)
    gdf_NUTS = gdf_NUTS.to_crs(3035)
    # Add area_NUTS [km2]
    gdf_NUTS['area_NUTS'] = gdf_NUTS.area/1e6


    ##### Make intersection, and group by NUTS
    intersected = gpd.overlay(gdf_network_storage_units, gdf_NUTS, how='intersection')
    # Get intersected area
    intersected['area_intersection'] = intersected.geometry.area
    # Get weighted p_nom according to percentage of intersected areas
    intersected['weighted_p_nom'] = intersected['p_nom'] * (intersected['area_intersection'] / intersected['area']/1e6) # 'area' refers to Voronoi cell


    df_p_nom = intersected.groupby('NUTS_ID')['weighted_p_nom'].sum().reset_index()



    ##### Merge gdf_NUTS and df_p_nom
    gdf_NUTS_storage_units = pd.merge(gdf_NUTS, df_p_nom, on='NUTS_ID')
    # Add more columns
    gdf_NUTS_storage_units['weighted_p_nom_density'] = gdf_NUTS_storage_units['weighted_p_nom'] / gdf_NUTS_storage_units['area_NUTS']

    
    gdf_NUTS_storage_units = gdf_NUTS_storage_units.to_crs('4036')



    return gdf_NUTS_storage_units


