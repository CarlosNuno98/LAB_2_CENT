# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 23:20:41 2020

@author: carlo
"""

# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Carlos Nuño
# -- repositorio: https://github.com/CarlosNuno98/LAB_2_CENT
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np

# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Obtener un 


def f_leer_archivo(param_archivo):
    '''

    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer
    
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    
    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    '''

    # Leer archivo de datos y guardarlo en un DataFrame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Hoja1')

    # elegir solo renglones en los que la columna type == buy | type == sell

    # Convertir en minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]
    # Asegurar que ciertas son del tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
              'taxes', 'order']

    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    #print(df_data)
    return df_data
# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular el tamaño de los pips por instrumento

def f_pip_size(param_ins):
    """
       Parameters
       ----------
       param_ins : str : nombre de instrumento
       Returns
       -------
       Debugging
       -------
       param_ins = 'usdjpy'
       """

    # encontrar y eliminar un guion bajo
    # inst = param_ins.replace('_', '')

    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,
                 'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                 'audusd': 10000, 'nzdusd': 10000,
                 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000,
                 'audnzd': 10000, 'nzdcad': 10000, 'audcad': 10000,
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pips_inst[inst]

# -- ------------------------------------------------------ FUNCION: Columna tiempos -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Segundos que permanecio cada operacion abierta

# Importamos las librerias necesarias para crear esta funcion

from datetime import  datetime
from datetime import timedelta


# Se crea la funcion

def f_columnas_tiempos(datos):
    '''
    Parameters
    ----------
    datos : DataFrame con la informaciona utilizar
    
    Returns
    -------
    datos: con informacion contenida en archivo leido
    
    Debugging
    ---------
    datos = 'archivo_tradeview_1.xlsx'

    '''

    # Se toman las columnas de tiempo en donde se abrio y cerro la posicion y creamos un nuevo DataFrame con estas columnas
    
    df_new = datos[['opentime','closetime']]
    df = pd.DataFrame(data=df_new)
    df['opentime'] = pd.to_datetime(df_new['opentime'])
    df['closetime'] = pd.to_datetime(df_new['closetime'])

    # Se crea una nueva variable que resta los tiempos y despues los convertimos a segundos para al final agragarlos al DataFrame original
    
    Time = df['closetime'] - df['opentime']
    Time = Time.dt.seconds
    Time = pd.DataFrame(Time)
    datos['Time'] = Time
    return datos

# -- ------------------------------------------------------ FUNCION: Columna pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Pips obtenidos en cada operacion

def f_columnas_pips(datos):
    '''

    Parameters
    ----------
    datos : df con la informaciona utilizar
    
    Returns
    -------
    datos: con informacion obtenida de la funcion
    
    Debugging
    ---------
    datos = 'archivo_tradeview_1.xlsx'

    '''
    
    # Se creo un nuevo DataFrame con las columnas que se iban a necesitar
    Pips = datos[['symbol','type','openprice','closeprice']]
    Pips.index = np.arange(0,len(Pips))
    
    pip = []
    contador = 0
    
    # Entramos a un ciclo donde dependiendo del type y si es buy o sell es lo que la funcion hara e ira guardando los resultados en un nuevo arreglo
    
    for i in range(0,len(Pips)):
        if Pips['type'][i] == 'buy':
            f = Pips['symbol'][contador]
            multiplicador = f_pip_size(param_ins = f)
            pip.append((Pips['closeprice'][i] - Pips['openprice'][i]) * multiplicador)
        else:
            f = Pips['symbol'][contador]
            multiplicador = f_pip_size(param_ins = f)
            pip.append((Pips['openprice'][i] - Pips['closeprice'][i])*multiplicador)
        contador = contador + 1
           
    # El arreglo se convierte en un DataFrame que despues sera agregado a nuestro DataFrame original
    
    Pips = pd.DataFrame(pip)
    datos['Pips'] = Pips
    return datos

# -- ------------------------------------------------------ FUNCION: estadisticas_ba -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Diccionario con 2 tablas: da_1_tabla y df_1_ranking 


def f_estadisticas_ba(datos):
    '''
    Parameters
    ----------
    datos : DataFrame con la informaciona utilizar
    
    Returns
    -------
    df_1_tabla : DataFrame con calculos sobre el comportmaiento de la cuenta
    df_1_ranking: DataFrame con ratio de efectividad de operaciones realizadas
    
    Debugging
    ---------
    datos = 'archivo_tradeview_1.xlsx'

    '''
    
    #df_1_tabla
    
    Pips = datos[['symbol','type','openprice','closeprice']]
    Pips.index = np.arange(0,len(Pips))
    Win = 0   #Ganadoras
    Lose = 0  #Perdedoras
    WinB = 0  #Ganadoras Compra
    WinS = 0 #Ganadoras de Venta
    LoseB = 0 #Perdedora Compra
    LoseS = 0 #Perdedoras Venta


    # Entramos a un ciclo en donde iremos contando los trades ganados y los perdidos y se iran agregando a la variable correspondiente

    for i in range(0,len(datos)):
        if datos['type'][i] == 'buy':
            if datos['Pips'][i] > 0:
                Win = Win + 1
                WinB = WinB + 1
            else:
                Lose = Lose + 1 
                LoseB = LoseB + 1
        else:
            if datos['Pips'][i] > 0:
                Win = Win + 1
                WinS = WinS + 1
            else:
                Lose = Lose + 1 
                LoseS = LoseS + 1

    # Se realizan las operaciones necesarias para poder obtener los resultados(divisiones, promedios...)

    Ops_totales = len(Pips)
    r_efectividad  = Win / Ops_totales
    r_porcion = Lose / Win
    r_efectividad_c = WinB / Ops_totales
    r_efectividad_v = WinS / Ops_totales
    Media_Profit = datos['profit'].mean()
    Media_Pips = datos['Pips'].mean()

    #Creamos una tabla en donde mostremos los resultados con sus respectivos nombres de las variables

    df_1_tabla = pd.DataFrame (columns = ['Medida','Valor','Descripcion'])
    df_1_tabla.Medida = ['Ops totales','Ganadoras','Ganadoras_c','Ganadoras_v','Perdedoras','Perdedoras_c','Perdedoras_v','Media (Profit)','Media (Pips)','r_efectividad','r_proporcion','r_efectividad_c','r_efectividad_v']
    df_1_tabla.Descripcion = ['Operaciones totales','Operaciones ganadoras','Operaciones ganadoras de compra','Operaciones ganadoras de venta','Operaciones perdedoras','Operaciones perdedoras de compra','Operaciones perdedoras de venta','Mediana de profit de operaciones','Mediana de pips de operaciones','Ganadoras Totales/Operaciones Totales','Perdedoras Totales/Ganadoras Totales','Ganadoras Compras/Operaciones Totales','Ganadoras Ventas/ Operaciones Totales']
    df_1_tabla.Valor = [Ops_totales, Win, WinB, WinS, Lose, LoseB, LoseS, Media_Profit, Media_Pips , r_efectividad, r_porcion, r_efectividad_c, r_efectividad_v,]
    
    #df_1_ranking
    
    # Se agrupan los valores de item donde se cuentan cuales fueron mayores a 1 en el profit para identificar que son ganadoras

    efec = datos[['symbol','profit']]
    count_movi = efec.groupby('symbol').count()
    count_posit = efec[efec['profit'] > 0].groupby([efec['symbol']])
    count_posit = count_posit.count()

    # Se dividen las posiciones ganadas entre las totales y se multiplican por 100 para obtenerlo en porcentaje

    Efectividad = ((count_posit['profit'] / count_movi['profit'] ) * 100).round(4)
    Efectividad = pd.DataFrame(Efectividad)
    Efectividad_1 = pd.DataFrame(Efectividad)
    Porcentaje  = [str(l) + "%" for l in Efectividad.profit]
    Efectividad.profit = Porcentaje

    # Creamos un nuevo DaraFrame con los resultados obtenidos

    Ratio_efect = pd.DataFrame(Porcentaje)
    Efectividad.rename(columns = {'profit':'rank'})
    New = Efectividad.reset_index()
    df_1_ranking = New.rename(columns={'symbol':'symbol'})
    
    #Juntamos todo en un diccionario que sera lo que nos devolvera la funcion
    
    Diccionario = {"Estadistica":df_1_tabla,"Efectividad":df_1_ranking}  
    return Diccionario

# -- ------------------------------------------------------ FUNCION: capital_acm -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Evolucion de capital de la cuenta de trading
    
def capital_acm(datos): 
    '''
    Parameters
    ----------
    datos : DataFrame con la informaciona utilizar
    
    Returns
    -------
    Capital_acm : Columna en datos con el capital acumulado
    
    Debugging
    ---------
    datos = 'archivo_tradeview_1.xlsx'

    '''
    capital = 5000
    capital_acm = []
    
    # Creamos un ciclo en donde se estara sumando o restando el capital con la posicion realizada
    
    for i in range(0,len(datos)):
        capital = datos['profit'][i] + capital
        capital_acm.append(capital)

    Capital_acm = pd.DataFrame(capital_acm)
    datos['Capital_acm'] = Capital_acm
    return datos

# -- ------------------------------------------------------ FUNCION: f_profit_diario -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Evolucion de capital de la cuenta de trading


def f_profit_diario(datos): 
    '''
    Parameters
    ----------
    datos : DataFrame con la informaciona utilizar
    
    Returns
    -------
    f_profit_diario: DataFrame con fechas, profit diario y profit diario acumulado
    
    Debugging
    ---------
    datos = 'archivo_tradeview_1.xlsx'

    '''
    # Agrupamos las fechas en las que se hicieron transacciones para despues sumar los profit obtenemos en las operaciones diarias
    # Para despues agruparlos en los profit_acm_d donde si no hubo ganancia o perdida ese dia se pone el valor del dia anterior
    Fechas = [datos["closetime"][l][:10] for l in range(datos.shape[0])]
    timestamp = pd.DataFrame(columns = ('timestamp','profit_d'))
    timestamp.timestamp = Fechas
    timestamp.profit_d = datos['profit']
    profit_diario = timestamp.groupby('timestamp').sum()
    profit_diario = profit_diario.reset_index()
    Fecha = pd.to_datetime(profit_diario['timestamp'])
    profit_diario['timestamp'] = Fecha

    profit_diario_1 = pd.DataFrame (columns = ['timestamp','profit_d'])
    profit_diario_1.timestamp = pd.date_range(start="2019.08.27",end="2019.09.25")

    df = pd.concat([profit_diario, profit_diario_1])
    df = df.reset_index(drop=True)

    Agrupados = df.groupby('timestamp')
    Agrupados = Agrupados.mean()
    f_profit_diario = Agrupados.fillna(0)
    
    # Comenzamos con un capital de 5000, donde se le iran sumando o restando las operaciones ganadoras o perdedoras
    f_profit_diario = f_profit_diario.reset_index()
    capital = 5000
    capital_acm_d = []
    for i in range(0,len(f_profit_diario)):
        capital = f_profit_diario['profit_d'][i] + capital
        capital_acm_d.append(capital)

    profit_acm_d = pd.DataFrame(capital_acm_d)
    f_profit_diario['profit_acm_d'] = profit_acm_d
    
    return f_profit_diario

# -- ------------------------------------------------------ FUNCION: f_estadisticas_mad-- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Medidas de atribucion al desempeño

def f_estadisticas_mad(datos): 
    '''
    Parameters
    ----------
    datos : DataFrame con la informaciona utilizar
    
    Returns
    -------
    MAD: Tabla con los valores obtenidos 
    
    Debugging
    ---------
    datos = 'archivo_tradeview_1.xlsx'

    '''
    datos_1 = f_profit_diario(datos)
    # rf y md diaria
    rf = .08 / 300
    mar = .3/300
    
    #Rendimientos de los logaritmos acumulados diarios
    rp_0 = np.log(datos_1['profit_acm_d']/datos_1['profit_acm_d'].shift(1))
    rp = np.mean(rp_0)
    sdp = rp_0.std()
    
    #Separamos las operaciones de compra de las de venta
    sell = datos.loc[datos['type'] == 'sell']
    buy = datos.loc[datos['type'] == 'buy']
    
    #Se obtienen los rendimientos de compra y venta con el mar señalado
    rend_sell = np.log(sell['Capital_acm'] / sell['Capital_acm'].shift(1))
    rp_sell = np.mean(rend_sell)
    mar_sell = rend_sell[rend_sell <= mar]
    
    rend_buy = np.log(buy['Capital_acm'] / buy['Capital_acm'].shift(1))
    rp_buy = np.mean(rend_buy)
    mar_buy = rend_buy[rend_buy <= mar]
        
    # Calculos de las medidas de atribución al desempeño
    sharpe = (rp - rf)/sdp
    sortino_c = (rp_buy-mar)/(mar_buy.std())*-1
    sortino_v = (rp_sell-mar)/(mar_sell.std())*-1
    drawdown_capi = 5 
    drawup_capi = 5
    information_r = 5 

    MAD = pd.DataFrame(columns = ('metrica','valor','descripcion'))
    MAD.metrica = ['sharpe','sortino_c','sortino_v','drawdown_capi','drawup_capi','information_r']
    MAD.valor = [sharpe,sortino_c,sortino_v,drawdown_capi,drawup_capi,information_r]
    MAD.descripcion = ['Sharpe Ratio','Sortino Ratio para Posiciones  de Compra','Sortino Ratio para Posiciones de Venta','DrawDown de Capital','DrawUp de Capital','Information Ratio']
    
    return MAD





