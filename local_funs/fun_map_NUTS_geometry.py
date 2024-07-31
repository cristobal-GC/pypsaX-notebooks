


import cartopy



def fun_map_NUTS_geometry(gdf_NUTS, ax):
    """
    This function adds geo information from gdf_NUTS in axes 'ax'
    """

    country_color = 'wheat'
    

    gdf_NUTS.to_crs('4036').plot(ax=ax,color=country_color, alpha=1, edgecolor='none')


    ### Add area
    gdf_NUTS.to_crs('4036').plot(ax=ax,color=country_color, alpha=1, edgecolor='black', lw=.1)
