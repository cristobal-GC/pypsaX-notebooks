



from fun_gdf_network_loads import fun_gdf_network_loads



def fun_map_network_loads(n, feature, ax):
    """
    This function plots load features in the geometry of a network.

    Features:
      - area
      - annual_load         : [TWh]
      - annual_load_density : [GWh/km2]      
    """

    gdf_network_loads = fun_gdf_network_loads(n)



    ##### Plot in map


    gdf_network_loads.plot(ax=ax, column=feature, cmap='viridis', edgecolor="black", legend=True, alpha=1)


    if feature=='area':
        total = gdf_network_loads[feature].sum()
        ax.set_title(f'Area. Total: {total:.2f} km2')

    if feature=='annual_load':
        total = gdf_network_loads[feature].sum()
        ax.set_title(f'Annual load. Total: {total:.2f} TWh')        

    if feature=='annual_load_density':
        ax.set_title(f'Annual load density [GWh/km2]')

