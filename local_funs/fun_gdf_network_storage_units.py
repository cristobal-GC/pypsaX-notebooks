

import pandas as pd



def fun_gdf_network_storage_units(carrier, n):
    """
    This function provides a gdf of a network with some storage unit features 
    for a specific carrier.

    Columns:
      - geometry
      - bus
      - carrier
      - area
      - p_nom               : installed capacity [MW]
      - p_nom_density       : ratio between p_nom and area [MW/km2]

    The gdf is provided in Plate Carrée crs('4036')    
    """

    ##### Get df with storage_units info
    su = n.storage_units
    # filter carrier
    df = su[su['carrier']==carrier]
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
 
    ##### Merge df and gdf
    gdf_network_storage_units =  pd.merge(gdf,df, on='bus')

    ##### Add p_nom_density 
    gdf_network_storage_units['p_nom_density'] = gdf_network_storage_units['p_nom'] / gdf_network_storage_units['area']




    return gdf_network_storage_units



