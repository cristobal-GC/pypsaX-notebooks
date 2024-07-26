

import cartopy



def fun_map_add_features(ax):

    ocean_color = 'none'

    ax.add_feature(cartopy.feature.BORDERS, color="black", linewidth=.5)
    ax.add_feature(cartopy.feature.COASTLINE, color="black", linewidth=.5)
    ax.add_feature(cartopy.feature.LAND,edgecolor='none')
    ax.add_feature(cartopy.feature.OCEAN,edgecolor='none', facecolor=ocean_color)
