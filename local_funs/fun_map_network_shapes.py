

import cartopy



def fun_map_network_shapes(n, ax, domain='both'):
    """
    This function adds geo information from n.shapes in axes 'ax'

    Voronoi cells are added with a borderline

    Country and offshore regions are added with an area
    
    Domain: 'onshore' , 'offshore' , 'both' 
    """

    country_color = 'wheat'
    offshore_color = 'aliceblue' # 'azure'


    if domain=='onshore' or domain=='both':

        ### Add country (area)
        n.shapes.loc[(n.shapes['type']=='country') & (n.shapes['component']=='')
                    ].plot(ax=ax,color=country_color,alpha=1,edgecolor='none')

        ### Add Voronoi onshore cells (line)
        n.shapes.loc[(n.shapes['type']=='onshore') & (n.shapes['component']=='Bus')
                    ].plot(ax=ax,color='none',alpha=1,edgecolor='black',lw=.1)


    if domain=='offshore' or domain=='both':

        ### Add offshore (area)
        n.shapes.loc[(n.shapes['type']=='offshore') & (n.shapes['component']=='')
                    ].plot(ax=ax,color=offshore_color,alpha=1,edgecolor='none')

        ### Add Voronoi offshore cells (line)
        n.shapes.loc[(n.shapes['type']=='offshore') & (n.shapes['component']=='Bus')
                    ].plot(ax=ax,color='none',alpha=1,edgecolor='black',lw=.1)

