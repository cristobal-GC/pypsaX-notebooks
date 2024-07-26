

import cartopy



def fun_map_network_geometry(n, ax):

    country_color = 'wheat'
    offshore_color = 'aliceblue' # 'azure'


    ### Add country (area)
    n.shapes.loc[(n.shapes['type']=='country') & (n.shapes['component']=='')
                ].plot(ax=ax,color=country_color,alpha=1,edgecolor='none')

    ### Add offshore (area)
    n.shapes.loc[(n.shapes['type']=='offshore') & (n.shapes['component']=='')
                ].plot(ax=ax,color=offshore_color,alpha=1,edgecolor='none')

    ### Add Voronoi onshore cells (line)
    n.shapes.loc[(n.shapes['type']=='onshore') & (n.shapes['component']=='Bus')
                ].plot(ax=ax,color='none',alpha=1,edgecolor='black',lw=.1)

    ### Add Voronoi offshore cells (line)
    n.shapes.loc[(n.shapes['type']=='offshore') & (n.shapes['component']=='Bus')
                ].plot(ax=ax,color='none',alpha=1,edgecolor='black',lw=.1)

