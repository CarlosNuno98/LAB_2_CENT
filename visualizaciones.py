
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - para visualizacion de datos
# -- mantiene: Carlos Nuño
# -- repositorio: https://github.com/CarlosNuno98/LAB_2_CENT
# -- ------------------------------------------------------------------------------------ -- #

import matplotlib.pyplot as plt


# -- --------------------------------------------------------- GRÁFICA: df_1_ranking -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- --- Grafica de efectividad de los insturmentos

def df_1_ranking(f_estadisticas):
    labels = f_estadisticas['Efectividad']['symbol']
    sizes =  f_estadisticas['Efectividad']['profit']
    sizes = list(map(lambda sizes: sizes.replace("%",""), sizes))
    explode = (0, 0.1, 0.1, 0,0,0,0,0,0,0,0)
    plt.pie(sizes, explode=explode, labels = labels, shadow=True, startangle=140)
    plt.title('Ranking')
    plt.legend(loc = (1.3,.2))
    plt.xlabel('Grafico de ratio de efectividad de cada instrumento')
    plt.show()
