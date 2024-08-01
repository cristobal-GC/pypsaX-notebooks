

import pandas as pd



def fun_gdf_network_generators(carrier, n):
    """
    This function provides a gdf of a network with some generation features 
    for a specific carrier.

    Columns:
      - geometry
      - bus
      - carrier
      - area
      - p_nom               : installed capacity [MW]
      - p_nom_density       : ratio between p_nom and area [MW/km2]
      - p_nom_max           : potential according to land availability [MW]
      - p_nom_max_density   : ratio between p_nom_max and area [MW/km2]
      - p_nom_max_ratio     : ration between p_nom and p_nom_max [-]

    The gdf is provided in Plate Carrée crs('4036')    
    """

    ##### Get df with generators info
    gg = n.generators
    # filter carrier
    df = gg[gg['carrier']==carrier]
    # remove zero_capacities
    df = df.loc[ df['p_nom']>0 , ['carrier', 'bus', 'p_nom', 'p_nom_max']]


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
    gdf_network_generators =  pd.merge(gdf,df, on='bus')

    ##### Add p_nom_density 
    gdf_network_generators['p_nom_density'] = gdf_network_generators['p_nom'] / gdf_network_generators['area']

    ##### Add p_nom_max_density
    gdf_network_generators['p_nom_max_density'] = gdf_network_generators['p_nom_max'] / gdf_network_generators['area']

    ##### Add p_nom_max_ratio
    gdf_network_generators['p_nom_max_ratio'] = gdf_network_generators['p_nom'] / gdf_network_generators['p_nom_max']




    return gdf_network_generators



