########## Plot map at NUTS level

import pandas as pd
import geopandas as gpd


def fun_map_capacity_NUTS(carrier, token_density, n, gdf_NUTS, ax):
    """
    This function plots the installed capacity (or spatial density)
    of a generator carrier in NUTS regions
    """

    ##### Get df with capacity
    gg = n.generators
    # filter carrier
    df = gg[gg['carrier']==carrier]
    # remove zero_capacities
    df = df.loc[ df['p_nom']>0 , ['carrier', 'bus', 'p_nom']]


    ##### Get gdf with geometry
    if 'off' in carrier:
        gdf = n.shapes[ (n.shapes['type']=='offshore') & (n.shapes['component']=='Bus')].copy()
    else:
        gdf = n.shapes[ (n.shapes['type']=='onshore') & (n.shapes['component']=='Bus')].copy()

    gdf.rename(columns={'idx': 'bus'}, inplace=True)

    gdf = gdf[['geometry', 'bus']]


    ##### Merge
    gdf_merged = pd.merge(gdf,df, on='bus')
    # Put in crs (3035)
    gdf_merged = gdf_merged.to_crs(3035)


    ##### gdf_NUTS, retain relevant columns and add area
    gdf_NUTS = gdf_NUTS[['NUTS_ID', 'geometry']]
    # Put in crs (3035)
    gdf_NUTS = gdf_NUTS.to_crs(3035)
    # Add area [km2]
    gdf_NUTS['area'] = gdf_NUTS.area/1e6


    ##### Make intersection, and group by NUTS
    intersected = gpd.overlay(gdf_merged, gdf_NUTS, how='intersection')
    # Get intersected area
    intersected['area_intersection'] = intersected.geometry.area
    # Get weighted p_nom according to percentage of intersected areas
    intersected['weighted_p_nom'] = intersected['p_nom'] * (intersected['area_intersection'] / intersected['geometry'].area)

    p_nom_by_NUTS = intersected.groupby('NUTS_ID')['weighted_p_nom'].sum().reset_index()


    ##### get gdf_NUTS_merged, and capacity density, and get back to 4036 crs
    gdf_NUTS_merged = pd.merge(gdf_NUTS, p_nom_by_NUTS, on='NUTS_ID')
    gdf_NUTS_merged['weighted_p_nom_density'] = gdf_NUTS_merged['weighted_p_nom'] / gdf_NUTS_merged['area']
    gdf_NUTS_merged = gdf_NUTS_merged.to_crs('4036')



    ##### Plot in map

    gdf_NUTS.to_crs('4036').plot(ax=ax, edgecolor='black', lw=.1, alpha=1)


    if token_density == 0:
        gdf_NUTS_merged.plot(ax=ax, column='weighted_p_nom', cmap='viridis', edgecolor="black", legend=True, alpha=1)
        total_capacity = gdf_merged['p_nom'].sum()
        ax.set_title(f'{carrier} : Installed capacity [MW]. Total: {total_capacity:.2f}')

    if token_density == 1:
        gdf_NUTS_merged.plot(ax=ax, column='weighted_p_nom_density', cmap='viridis', edgecolor="black", legend=True, alpha=1)
        ax.set_title(f'{carrier} : Installed capacity density [MW/km2]')



