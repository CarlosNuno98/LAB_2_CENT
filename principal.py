
# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Carlos Nuño
# -- repositorio: https://github.com/CarlosNuno98/LAB_2_CENT
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vz

archivo = "archivo_tradeview_1.xlsx"
df_archivo = fn.f_leer_archivo(archivo)
datos = df_archivo
datos = fn.f_columnas_tiempos(datos)
datos = fn.f_columnas_pips(datos)
datos = fn.capital_acm(datos)

f_estadisticas = fn.f_estadisticas_ba(datos)
vz.df_1_ranking(f_estadisticas)

Profit_diario = fn.f_profit_diario(datos)


