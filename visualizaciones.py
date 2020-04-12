
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - para visualizacion de datos
# -- mantiene: Carlos Nuño
# -- repositorio: https://github.com/CarlosNuno98/LAB_2_CENT
# -- ------------------------------------------------------------------------------------ -- #

import matplotlib.pyplot as plt
import funciones as fn


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
    
def drawdown(datos):
    datos_1 = fn.f_profit_diario(datos)
    Draw_d_0 = datos_1[['timestamp','profit_acm_d']]
    Draw_d_0.set_index('timestamp', inplace=True)
    
    Draw_d_1 = Draw_d_0['profit_acm_d'].cummax()
    drawdown = (Draw_d_0['profit_acm_d'] - Draw_d_1 )/Draw_d_1
    plt.title('Drawdown')
    plt.ylabel('%')
    drawdown.plot(linestyle = '--', color = 'red')
    plt.show()