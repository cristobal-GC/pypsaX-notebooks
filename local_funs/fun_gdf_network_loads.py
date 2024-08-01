



import pandas as pd



def fun_gdf_network_loads(n):
    """
    This function provides a gdf of a network with some load features.

    Columns:
      - geometry
      - bus
      - carrier
      - area
      - annual_load         : [TWh]
      - annual_load_density : [GWh/km2]      

    The gdf is provided in Plate Carrée crs('4036')    
    """

    ##### Get df with load info
    lo_t = n.loads_t['p_set'].copy()
    df = lo_t.sum().to_frame(name='annual_load')
    
    # Put in TWh
    df['annual_load'] = df['annual_load'].div(1e6)

    # Add column 'bus'
    df['bus'] = df.index


    ##### Get gdf with geometry and area
    gdf = n.shapes[ (n.shapes['type']=='onshore') & (n.shapes['component']=='Bus')].copy()

    gdf.rename(columns={'idx': 'bus'}, inplace=True)

    gdf = gdf[['geometry', 'bus']]

    # Add area [km2]
    gdf_area = gdf.to_crs(3035)
    gdf['area'] = gdf_area.area/1e6

 
    ##### Merge df and gdf
    gdf_network_loads =  pd.merge(gdf,df, on='bus')

    ##### Add annual_load_density
    gdf_network_loads['annual_load_density'] = gdf_network_loads['annual_load'] / gdf_network_loads['area']
    # Put in GWh/km2
    gdf_network_loads['annual_load_density'] = gdf_network_loads['annual_load_density']*1e3



    return gdf_network_loads



