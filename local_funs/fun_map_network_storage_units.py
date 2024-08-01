

from fun_gdf_network_storage_units import fun_gdf_network_storage_units



def fun_map_network_storage_units(carrier, n, feature, ax):
    """
    This function plots storage unit features for a specific carrier
    in the geometry of a network.

    Features:
      - area
      - p_nom               : installed capacity [MW]
      - p_nom_density       : ratio between p_nom and area [MW/km2]
    """

    gdf_network_storage_units = fun_gdf_network_storage_units(carrier, n)



    ##### Plot in map


    gdf_network_storage_units.plot(ax=ax, column=feature, cmap='viridis', edgecolor="black", legend=True, alpha=1)


    if feature=='area':
        total = gdf_network_storage_units[feature].sum()
        ax.set_title(f'Area. Total: {total:.2f} km2')

    if feature=='p_nom':
        total = gdf_network_storage_units[feature].sum()
        ax.set_title(f'{carrier} : Installed capacity. Total: {total:.2f} MW')        

    if feature=='p_nom_density':
        ax.set_title(f'{carrier} : Installed capacity density [MW/km2]')

         


