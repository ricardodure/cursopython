import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import os
import datetime
from datetime import date
import sqlite3
import re

#------------------------------------------------------------------------------------------------------
# DEFINICIONES Y VARIABLES
#------------------------------------------------------------------------------------------------------
VENTANA = "1280x720+0+0"
DATABASE = "meses2023.db"
FUENTE = "Bahnschrift Condensed" # fuente que utilizaremos en el programa
FUENTE_LIGHT = "Bahnschrift Light Condensed" # fuente que utilizaremos en el programa
COLOR_BG = "#0E1B1E" # color de fondo de ventana
COLOR_BG_OSC = "#081012" # mas oscuro que color_bg
COLOR_INDICADORES_BG = "#005252" # color del fondo donde se muestran los indicadores
COLOR_GRIS_OSC = "#454545" # gris oscuro
COLOR_ACENTO_1 = "#FFB800" # acento amarillo
COLOR_ACENTO_2 = "#00E0E0" # acento cyan
COLOR_SEP = "#9E9E9E" # color de los separadores en root
COLOR_BORDE = "#00615E" # color de borde genérico para los elementos de root
COLOR_BTN_MES = "#2E7D86" # color de botones de meses

meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
meses_lc = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
totales_gastos = [0,0,0,0,0,0,0,0,0,0,0,0] # creo la lista que contendrá los gastos totales de todos los meses
totales_ops = [0,0,0,0,0,0,0,0,0,0,0,0] # creo la lista que contendrá el total de operaciones de todos los meses
sel_mes = 1 # por defecto seleccionamos enero aunque luego en ObtenerMesActual este valor se modifica.
sel_mes_nombre = meses[0] # traemos el nombre del mes, por defecto seleccionamos enero
sel_accion = 0 # accion que deberá realizar el boton de OK en el submenu de acciones (1-alta 2-editar) - el resto no utiliza submenu sino ventanas de 'askyesno'
sel_estadisticas = 0 # ventana que está actualmente seleccionada en Estadísticas
edit_id = 0 # defino la variable global de "id" que utilizará la funcion de editar

#------------------------------------------------------------------------------------------------------
# IMAGENES
#------------------------------------------------------------------------------------------------------
# Obtenemos el directorio base de todos los assets que usaré
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# cargamos las imagenes que vamos a utilizar desde el directorio "assets"
IM_FONDO_HD = os.path.join(BASE_DIR, "assets", "fondo_alpha.png")
IM_FONDO_FHD = os.path.join(BASE_DIR, "assets", "fondo_alpha_fhd.png")
IM_FONDO_ST = os.path.join(BASE_DIR, "assets", "fondo_estadisticas.png")

# CREAMOS LA BASE DE DATOS Y LAS TABLAS
#↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
#---------------------------------
# CREARBASE - Creamos la base ni bien inicia el programa, si no existe. Si existe solo se conectará a ella.
#---------------------------------
def crearBase(): 
    base = sqlite3.connect(DATABASE)
    return base
crearBase() # Y ejecutamos la funcion
#---------------------------------
# CHECKTABLAS - Checkeamos si las tablas de meses ya existen dentro de la base de datos, y sino, llamamos a crearTablas().
#---------------------------------
def checkTablas(base):
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    i = 0
    for mes in meses_lc: # iteramos entre la lista de meses y les vamos asignando los nombres a las tablas 
        tabla_mes = meses_lc[i]
        cursor = base.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla_mes}'") #sqlite_master es la base maestra que contiene las demas tablas (los meses en este caso)  
        existe = cursor.fetchone() # obtenemos el nombre de la tabla y luego usamos el resultado para determinar si existe o no.

        if existe: # podría haber usado una instruccion CREATE TABLE IF NOT EXISTS pero bueno, quería experimentar con sqlite_master
            # aca le digo que si la tabla existe, me traiga los datos ni bien inicia el programa para mostrarlos en el treeview correspondiente.
            traerdata = (f"SELECT * FROM {meses_lc[i]}")
            cursor.execute(traerdata)
            base.commit()
            rows = cursor.fetchall()

            for row in rows:
                listatablas[i].insert("", "end", values=row)
        else:
            # si no existe la tabla, la crea llamando a crearTablas
            crearTablas(base, tabla_mes)

        i += 1 # sumo 1 a "i" para iterar al siguiente mes
#---------------------------------
# CREARTABLAS - Esta funcion es llamada desde checkTablas(). Si las tablas no existen se crean desde aca.
#---------------------------------
def crearTablas(base, tabla_mes): 
    creartabla = (f"CREATE TABLE {tabla_mes}(id integer PRIMARY KEY AUTOINCREMENT, fecha text, concepto text(128), cantidad float(10), precio_u float(10), precio_t float(10))")
    cursor = base.cursor()
    cursor.execute(creartabla) # ejecutar la creacion de la tabla en la base de datos
    base.commit()
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
# FINALIZA SECCIÓN DE CREACIÓN DE BASE DE DATOS Y TABLAS.

#---------------------------------------------------------------------------------------------------------------
# FUNCIONES
#---------------------------------------------------------------------------------------------------------------

#+++++++++++++++++++++++++++++++++++++++++++++++++
# ObtenerMesActual - Función que corre una sola vez al iniciar el programa. Obtiene el mes actual y modifica la variable global sel_mes.
#+++++++++++++++++++++++++++++++++++++++++++++++++
def ObtenerMesActual():
        global sel_mes
        fecha = datetime.date.today()
        mes_actual = fecha.month
        sel_mes = mes_actual
        return mes_actual
#+++++++++++++++++++++++++++++++++++++++++++++++++
# ObtenerGastos - Obtengo los gastos de todos los meses y los guardo en una lista para luego mostrarlos en las estadisticas
#+++++++++++++++++++++++++++++++++++++++++++++++++
def ObtenerGastos():
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    columna_total = 5
    total = 0
    i = 0
    # sumo todos los valores de cada fila en la columna de "costo total".
    for elm in listatablas:
        total = 0 # por cada gasto de cada mes, reseteo el total a 0 para que no me sume TODOS los meses
        for row in listatablas[i].get_children(): # buscamos en columna "monto total" del mes en el que se encuentre el bucle
            valor = float(listatablas[i].item(row, 'values')[columna_total])
            total += valor

        totales_gastos[i]=total # una vez salimos del bucle del mes actual, agrego ese total final a la lista de totales de cada mes.
        i += 1
    return total
#+++++++++++++++++++++++++++++++++++++++++++++++++
# ObtenerOps - Obtengo el total de operaciones de todos los meses y los guardo en una lista para luego mostrarlos en las estadisticas
#+++++++++++++++++++++++++++++++++++++++++++++++++
def ObtenerOps():
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    operaciones = 0
    i = 0
    # busco la cantidad de filas en todos los treeview
    for elm in listatablas:
        operaciones = 0 # por cada total de operaciones de cada mes, reseteo el total a 0 para que no me sume TODOS los meses
        for row in listatablas[i].get_children():
            operaciones += 1

        totales_ops[i]=operaciones # una vez salimos del bucle del mes actual, agrego ese total final a la lista de totales de cada mes.
        i += 1
    return operaciones
#+++++++++++++++++++++++++++++++++++++++++++++++++
# reacomodarColumnas - Reacomodamos las columnas a sus anchos por defecto en caso de que el usuario las modifique.
#+++++++++++++++++++++++++++++++++++++++++++++++++
def reacomodarColumnas(): 
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    i = 0
    for tab in listatablas:
        #asignamos los atributos a las columnas
        listatablas[i].column("#0",width=0, minwidth= 0, stretch=tk.NO)
        listatablas[i].column("col_id",width=COLW_ID,minwidth=COLW_ID,anchor=W)
        listatablas[i].column("col_fecha",width=COLW_FECHA,minwidth=COLW_FECHA,anchor=W)
        listatablas[i].column("col_concepto",width=COLW_CONCEPTO,minwidth=COLW_CONCEPTO, anchor=W)
        listatablas[i].column("col_cantidad",width=COLW_CANTIDAD,minwidth=COLW_CANTIDAD,anchor=W)
        listatablas[i].column("col_costo_u",width=COLW_COSTO_U,minwidth=COLW_COSTO_U,anchor=W)
        listatablas[i].column("col_costo_t",width=COLW_COSTO_T,minwidth=COLW_COSTO_T,anchor=W)
        #asignamos los nombres a los headers de las columnas
        listatablas[i].heading("col_id",text=TXT_ID)
        listatablas[i].heading("col_fecha",text=TXT_FECHA)
        listatablas[i].heading("col_concepto",text=TXT_CONCEPTO)
        listatablas[i].heading("col_cantidad",text=TXT_CANTIDAD)
        listatablas[i].heading("col_costo_u",text=TXT_COSTO_U)
        listatablas[i].heading("col_costo_t",text=TXT_COSTO_T)
        i += 1
#+++++++++++++++++++++++++++++++++++++++++++++++++
# MostrarEstadisticas - Mostramos las estadísticas actualizadas
#+++++++++++++++++++++++++++++++++++++++++++++++++
def MostrarEstadisticas(ventana):
    # LLamamos a obtenerGastos y obtenerOps para calcular ambos y ubicarlos en las estadisticas
    ObtenerGastos()
    ObtenerOps()
    i = 0 # usado para los meses de los cuadros de estadisticas
    j = 0 # usado para los separadores de los cuadros
    global sel_estadisticas # ventana actual seleccionada. es persistente para cuando cerramos la ventana de estadisticas

    # obtenemos los gastos de cada mes desde la lista de totales que generamos en ObtenerGastos()
    gto_mes_1 = totales_gastos[0]
    gto_mes_2 = totales_gastos[1]
    gto_mes_3 = totales_gastos[2]
    gto_mes_4 = totales_gastos[3]
    gto_mes_5 = totales_gastos[4]
    gto_mes_6 = totales_gastos[5]
    gto_mes_7 = totales_gastos[6]
    gto_mes_8 = totales_gastos[7]
    gto_mes_9 = totales_gastos[8]
    gto_mes_10= totales_gastos[9]
    gto_mes_11= totales_gastos[10]
    gto_mes_12= totales_gastos[11]

    # obtenemos las operaciones de cada mes desde la lista de operaciones que generamos en ObtenerOps()
    ops_mes_1 = totales_ops[0]
    ops_mes_2 = totales_ops[1]
    ops_mes_3 = totales_ops[2]
    ops_mes_4 = totales_ops[3]
    ops_mes_5 = totales_ops[4]
    ops_mes_6 = totales_ops[5]
    ops_mes_7 = totales_ops[6]
    ops_mes_8 = totales_ops[7]
    ops_mes_9 = totales_ops[8]
    ops_mes_10= totales_ops[9]
    ops_mes_11= totales_ops[10]
    ops_mes_12= totales_ops[11]

    # deshabilito los botones de los meses y ademas el boton de estadisticas
    deshabilitarMeses(1)

    # Creo las listas de barras, textos, totales y cantidades para ubicarlas en los cuadros mediante un bucle.
    # Gastos - lista de los labels de las barras del cuadro
    st_gto_barras = [bg_st_gto_1,bg_st_gto_2,bg_st_gto_3,bg_st_gto_4,bg_st_gto_5,bg_st_gto_6,bg_st_gto_7,bg_st_gto_8,bg_st_gto_9,bg_st_gto_10,bg_st_gto_11,bg_st_gto_12]
    # Gastos - lista de los labels de los nombres de los meses del cuadro
    st_gto_textos = [txt_st_gto_mes_1,txt_st_gto_mes_2,txt_st_gto_mes_3,txt_st_gto_mes_4,txt_st_gto_mes_5,txt_st_gto_mes_6,txt_st_gto_mes_7,txt_st_gto_mes_8,txt_st_gto_mes_9,txt_st_gto_mes_10,txt_st_gto_mes_11,txt_st_gto_mes_12]
    # Gastos - lista de los totales mensuales que adquirí arriba, se utilizan para calcular la altura de las barras
    st_gto_totales = [gto_mes_1,gto_mes_2,gto_mes_3,gto_mes_4,gto_mes_5,gto_mes_6,gto_mes_7,gto_mes_8,gto_mes_9,gto_mes_10,gto_mes_11,gto_mes_12]
    # Gastos - lista de las cantidades que aparecen debajo del cuadro (en forma de enteros)
    st_gto_cantidades = [txt_st_gto_qty_1,txt_st_gto_qty_2,txt_st_gto_qty_3,txt_st_gto_qty_4,txt_st_gto_qty_5,txt_st_gto_qty_6,txt_st_gto_qty_7,txt_st_gto_qty_8,txt_st_gto_qty_9,txt_st_gto_qty_10,txt_st_gto_qty_11,txt_st_gto_qty_12]
    # Gastos - cantidades que aparecen a la izquierda del cuadro en los separadores
    st_gto_cantidades2 = [txt_st_gto_qty_1a,txt_st_gto_qty_2a,txt_st_gto_qty_3a,txt_st_gto_qty_4a]
    # Gastos - porcentajes que aparecen a la izquierda del cuadro en los separadores
    st_gto_porcentajes = [txt_st_gto_qty_1b,txt_st_gto_qty_2b,txt_st_gto_qty_3b,txt_st_gto_qty_4b]
     # Gastos - separadores del cuadro
    st_gto_separadores = [bg_estadisticas_gto_sep1, bg_estadisticas_gto_sep2, bg_estadisticas_gto_sep3, bg_estadisticas_gto_sep4]

    # Operaciones - lista de los labels de las barras del cuadro
    st_ops_barras = [bg_st_ops_1,bg_st_ops_2,bg_st_ops_3,bg_st_ops_4,bg_st_ops_5,bg_st_ops_6,bg_st_ops_7,bg_st_ops_8,bg_st_ops_9,bg_st_ops_10,bg_st_ops_11,bg_st_ops_12]
    # Operaciones - lista de los labels de los nombres de los meses del cuadro
    st_ops_textos = [txt_st_ops_mes_1,txt_st_ops_mes_2,txt_st_ops_mes_3,txt_st_ops_mes_4,txt_st_ops_mes_5,txt_st_ops_mes_6,txt_st_ops_mes_7,txt_st_ops_mes_8,txt_st_ops_mes_9,txt_st_ops_mes_10,txt_st_ops_mes_11,txt_st_ops_mes_12]
    # Operaciones - lista de los totales mensuales que adquirí arriba, se utilizan para calcular la altura de las barras
    st_ops_totales = [ops_mes_1,ops_mes_2,ops_mes_3,ops_mes_4,ops_mes_5,ops_mes_6,ops_mes_7,ops_mes_8,ops_mes_9,ops_mes_10,ops_mes_11,ops_mes_12]
    # Operaciones - lista de las cantidades que aparecen debajo del cuadro (en forma de enteros)
    st_ops_cantidades = [txt_st_ops_qty_1,txt_st_ops_qty_2,txt_st_ops_qty_3,txt_st_ops_qty_4,txt_st_ops_qty_5,txt_st_ops_qty_6,txt_st_ops_qty_7,txt_st_ops_qty_8,txt_st_ops_qty_9,txt_st_ops_qty_10,txt_st_ops_qty_11,txt_st_ops_qty_12]
    # Operaciones - cantidades que aparecen a la izquierda del cuadro en los separadores
    st_ops_cantidades2 = [txt_st_ops_qty_1a,txt_st_ops_qty_2a,txt_st_ops_qty_3a,txt_st_ops_qty_4a]
    # Operaciones - porcentajes que aparecen a la izquierda del cuadro en los separadores
    st_ops_porcentajes = [txt_st_ops_qty_1b,txt_st_ops_qty_2b,txt_st_ops_qty_3b,txt_st_ops_qty_4b]
     # Operaciones - separadores del cuadro
    st_ops_separadores = [bg_estadisticas_ops_sep1, bg_estadisticas_ops_sep2, bg_estadisticas_ops_sep3, bg_estadisticas_ops_sep4]

    # obtengo el mayor valor de gastos y operaciones para utilizarlos como referencia.
    mayor_valor_gto = max(totales_gastos)
    mayor_valor_ops = max(totales_ops)
    # si no existen operaciones o gastos cargados aún, obtendríamos un error de division por cero. En ese caso le digo que convierta los mayores a 1.
    if mayor_valor_gto == 0:
        mayor_valor_gto = 1
    if mayor_valor_ops == 0:
        mayor_valor_ops = 1
    # si la suma de operaciones de todos los meses es 0, mostramos el cartel de "sin operaciones" en los cuadros de estadísticas
    if sum(totales_ops) == 0:
        bg_estadisticas_gto_adv.place(x= 0, y=10, relwidth=1,relheight=0.76)
        bg_estadisticas_ops_adv.place(x= 0, y=10, relwidth=1,relheight=0.76)
    else: # de otra forma los ocultamos
        bg_estadisticas_gto_adv.place(x= 0, y=0, relwidth=0,relheight=0)
        bg_estadisticas_ops_adv.place(x= 0, y=0, relwidth=0,relheight=0)

    # Mostramos la ventana principal de las estadisticas
    bg_estadisticas_parent.place(x=320,y=58,width=922,height=610) # (x=320,y=58,width=922,height=610)

    if ventana == 0: # Ventana 0 es el cuadro de "Gastos"
        actualizarRegistro("Se muestran las estadísticas de gastos totales por mes.")
        j = 0
        sel_estadisticas = 0
        bg_estadisticas_gto_parent.place(x=2,y=70,width=910,height=530) # mostramos la parte de gastos
        bg_estadisticas_ops_parent.place(x=0,y=0,width=0,height=0) # escondemos la parte de operaciones

        btn_estadisticas_gto.config(state="disabled", bg= "lightgray", cursor="arrow")
        btn_estadisticas_ops.config(state="normal", bg= COLOR_BTN_MES, cursor="hand2")

        # Ubicamos los separadores y las cantidades de la izquierda en los cuadros
        for sep in range(4): # son 4 separadores
            # posiciono los separadores del cuadro
            st_gto_separadores[j].place(x=10,y=CUADRO_SEP_Y + (CUADRO_SEP * j),width=890,height=1)
            # posiciono las cantidades a la izquierda del cuadro para cada separador
            st_gto_cantidades2[j].place(x=0,y=CUADRO_SEP_Y + (CUADRO_SEP * j)-CUADRO_SEP + 12,width=64,height=20)
            # busco los porcentajes respecto al mayor valor (100%, 75, 50 y 25) y les asigno el texto a las cantidades
            st_gto_cantidades2[j].config(text=str(f"${int(mayor_valor_gto * (1 - (0.25 * j)))}"))
            # posiciono los indicadores de porcentaje (los textos de 100%, 75%, etc) junto a los separadores del cuadro.
            st_gto_porcentajes[j].place(x=0,y=CUADRO_SEP_Y + (CUADRO_SEP * j)-CUADRO_SEP + 35,width=64,height=20)
            j += 1
        # Calculamos las barras de los cuadros
        for mes in range(12): # son 12 meses
            """hice este algoritmo para calcular el alto de cada barra
            gto_mes * 100 / mayor_valor / 100"""
            # calculo el alto de las barras de los cuadros en base al algoritmo que toma el mayor valor.
            st_gto_barras[i].place(x=ST_CUADRO_BAR_X + (ST_CUADRO_BAR_SEP * i),rely=1 - (st_gto_totales[i] * 100 / mayor_valor_gto / 100),width=ST_CUADRO_BAR_W,relheight=(st_gto_totales[i] * 100 / mayor_valor_gto / 100))
            # posiciono los nombres de los meses debajo del cuadro
            st_gto_textos[i].place(x=ST_CUADRO_TXT_X + (ST_CUADRO_TXT_SEP * i),y=ST_CUADRO_TXT_Y,width=ST_CUADRO_TXT_W,height=ST_CUADRO_TXT_H)
            # posiciono las cantidades debajo de los nombres de los meses
            st_gto_cantidades[i].place(x=ST_CUADRO_TXT_QTY_X + (ST_CUADRO_TXT_QTY_SEP * i),y=ST_CUADRO_TXT_Y + 22,width=ST_CUADRO_TXT_QTY_W,height=ST_CUADRO_TXT_H)
            # asignamos el valor de cada cantidad por mes, y lo mostramos.
            st_gto_cantidades[i].config(text=(f"${int(totales_gastos[i])}"))

            i += 1

    elif ventana == 1: # Ventana 0 es el cuadro de "Operaciones"
        actualizarRegistro("Se muestran las estadísticas de operaciones realizadas por mes.")
        j = 0
        sel_estadisticas = 1
        bg_estadisticas_gto_parent.place(x=0,y=0,width=0,height=0) # escondemos la parte de gastos
        bg_estadisticas_ops_parent.place(x=2,y=70,width=910,height=530) # mostramos la parte de operaciones

        btn_estadisticas_gto.config(state="normal", bg= COLOR_BTN_MES, cursor="hand2")
        btn_estadisticas_ops.config(state="disabled", bg= "lightgray", cursor="arrow")

        # Ubicamos los separadores y las cantidades de la izquierda en los cuadros
        for sep in range(4): # son 4 separadores
            # posiciono los separadores del cuadro
            st_ops_separadores[j].place(x=10,y=CUADRO_SEP_Y + (CUADRO_SEP * j),width=890,height=1)
            # posiciono las cantidades a la izquierda del cuadro para cada separador
            st_ops_cantidades2[j].place(x=0,y=CUADRO_SEP_Y + (CUADRO_SEP * j)-CUADRO_SEP + 12,width=64,height=20)
            # busco los porcentajes respecto al mayor valor (100%, 75, 50 y 25) y les asigno el texto a las cantidades
            st_ops_cantidades2[j].config(text=float(mayor_valor_ops * (1 - (0.25 * j))))
            # posiciono los indicadores de porcentaje (los textos de 100%, 75%, etc) junto a los separadores del cuadro.
            st_ops_porcentajes[j].place(x=0,y=CUADRO_SEP_Y + (CUADRO_SEP * j)-CUADRO_SEP + 35,width=64,height=20)
            j += 1
        # Calculamos las barras de los cuadros
        for mes in range(12): # son 12 meses
            # calculo el alto de las barras de los cuadros en base al algoritmo que toma el mayor valor.
            st_ops_barras[i].place(x=ST_CUADRO_BAR_X + (ST_CUADRO_BAR_SEP * i),rely=1 - (st_ops_totales[i] * 100 / mayor_valor_ops / 100),width=ST_CUADRO_BAR_W,relheight=(st_ops_totales[i] * 100 / mayor_valor_ops / 100))
            # posiciono los nombres de los meses debajo del cuadro
            st_ops_textos[i].place(x=ST_CUADRO_TXT_X + (ST_CUADRO_TXT_SEP * i),y=ST_CUADRO_TXT_Y,width=ST_CUADRO_TXT_W,height=ST_CUADRO_TXT_H)
            # posiciono las cantidades debajo de los nombres de los meses
            st_ops_cantidades[i].place(x=ST_CUADRO_TXT_QTY_X + (ST_CUADRO_TXT_QTY_SEP * i),y=ST_CUADRO_TXT_Y + 22,width=ST_CUADRO_TXT_QTY_W,height=ST_CUADRO_TXT_H)
            # asignamos el valor de cada cantidad por mes, y lo mostramos.
            st_ops_cantidades[i].config(text=(f"{int(totales_ops[i])}"))

            i += 1

#+++++++++++++++++++++++++++++++++++++++++++++++++
# CerrarEstadisticas - Ocultamos la ventana de estadísticas
#+++++++++++++++++++++++++++++++++++++++++++++++++
def CerrarEstadisticas():
    # Ocultamos la ventana principal de las estadisticas
    bg_estadisticas_parent.place(x=0,y=0,width=0,height=0)
    habilitarMeses()

#+++++++++++++++++++++++++++++++++++++++++++++++++
# deshabilitarMeses - Deshabilito los botones de los meses, con la opcion de tambien deshabilitar el boton de estadisticas
#+++++++++++++++++++++++++++++++++++++++++++++++++
def deshabilitarMeses(estadisticas=0):
    # Obtengo los botones de los meses para cambiarles el color y deshabilitarlos
    listameses = [btn_mes1, btn_mes2, btn_mes3, btn_mes4, btn_mes5, btn_mes6, btn_mes7, btn_mes8, btn_mes9, btn_mes10, btn_mes11, btn_mes12]
    m = 0 # mes
    for mes in listameses: # deshabilito los botones de meses
        listameses[m].config(bg=COLOR_GRIS_OSC, state="disabled", cursor="arrow", disabledforeground="gray")
        m += 1
    if estadisticas == 1:
        boton_estadisticas.config(bg=COLOR_GRIS_OSC, state="disabled", cursor="arrow") # deshabilito el boton de estadisticas

#+++++++++++++++++++++++++++++++++++++++++++++++++
# habilitarMeses - Habilito los botones de los meses y el de estadísticas
#+++++++++++++++++++++++++++++++++++++++++++++++++
def habilitarMeses():
    global sel_mes
    # Obtengo los botones de los meses para cambiarles el color y habilitarlos nuevamente
    listameses = [btn_mes1, btn_mes2, btn_mes3, btn_mes4, btn_mes5, btn_mes6, btn_mes7, btn_mes8, btn_mes9, btn_mes10, btn_mes11, btn_mes12]
    m = 0 # mes
    for mes in listameses: # deshabilito los botones de meses
        listameses[m].config(bg=COLOR_BTN_MES, state="normal", cursor="hand2")
        m += 1
    boton_estadisticas.config(bg="cyan", state="normal", cursor="hand2") # habilito el boton de estadisticas
    # le devuelvo el color de resaltado al boton del mes seleccionado y lo deshabilito
    listameses[sel_mes-1].config(bg=COLOR_ACENTO_1, state="disabled", cursor="arrow", disabledforeground="black") 

#+++++++++++++++++++++++++++++++++++++++++++++++++
# deshabilitarTablas - Deshabilitamos los treeview
#+++++++++++++++++++++++++++++++++++++++++++++++++
def deshabilitarTablas():
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    # les cambio el color a los headers y fondo de los treeview para que luzcan deshabilitados
    estilo.configure("Treeview.Heading", background=COLOR_BG_OSC, foreground=COLOR_GRIS_OSC, font=(FUENTE, 12)) 
    estilo.configure("Treeview", fieldbackground=COLOR_GRIS_OSC, background=COLOR_GRIS_OSC, foreground="black", font=(FUENTE_LIGHT, 12)) 

    for tabla in listatablas:
        tabla["selectmode"] = "none" # deshabilitamos la seleccion de filas

#+++++++++++++++++++++++++++++++++++++++++++++++++
# habilitarTablas - Habilitamos los treeview
#+++++++++++++++++++++++++++++++++++++++++++++++++
def habilitarTablas():
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    # les devuelvo sus estilos originales a los treeview ya que ahora se encuentran habilitados
    estilo.configure("Treeview.Heading", background=COLOR_BG, foreground="white", font=(FUENTE, 12)) # configuro el estilo de los headers de todos los treeview
    estilo.configure("Treeview", fieldbackground="gray", background="gray", foreground="black", font=(FUENTE_LIGHT, 12)) # configuro el estilo de todos los treeview (fondo, fuente, etc)

    for tabla in listatablas:
        tabla["selectmode"] = "extended" # habilitamos nuevamente la seleccion de filas asignandole a cada tabla selectmode = extended

#+++++++++++++++++++++++++++++++++++++++++++++++++
# actualizarRegistro - Actualizamos el registro de actividad
#+++++++++++++++++++++++++++++++++++++++++++++++++
def actualizarRegistro(texto):
    ahora = datetime.datetime.now() # obtengo la hora actual usando el modulo datetime
    hora_actual = ahora.strftime("%H:%M:%S") # uso string format time para darle formato de hh mm ss

    bg_registro.config(text=(f"{hora_actual} - {texto}")) # actualizo el texto del registro de actividad

#+++++++++++++++++++++++++++++++++++++++++++++++++
# actualizarIndicadores - Actualizamos los indicadores de la barra de contenido
#+++++++++++++++++++++++++++++++++++++++++++++++++
def actualizarIndicadores():
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    columna_total = 5
    total = 0
    global sel_mes_nombre
    global sel_mes

    # sumo todos los valores de cada fila en la columna de "costo total".
    for row in listatablas[sel_mes-1].get_children():
        valor = float(listatablas[sel_mes-1].item(row, 'values')[columna_total])
        total += valor
     # actualizo el indicador de gastos totales de ese mes
    bar_gastos.config(text=f"${total:.2f}")
     # actualizo el texto del contador de operaciones en la barra de subtitulo
    bar_operaciones.config(text=str(len(listatablas[sel_mes-1].get_children())))
     # actualizo el indicador de mes
    bar_mes_actual.config(text=f"{sel_mes_nombre}") 
    # si no se encuentra ningun "child" (es decir, no tiene filas) entendemos que la tabla esta vacia y mostramos un indicador.
    if not listatablas[sel_mes-1].get_children():
        header_vacia.place(x=330,y=342,width=876,height=100)
    else:
        header_vacia.place(x=0,y=0,width=0,height=0)

    return total

#+++++++++++++++++++++++++++++++++++++++++++++++++
# actualizarTablas - Lanzamos un evento que limpia los treeview y luego los vuelve a llenar con la data actualizada desde la base de datos. esto sucede por cada abm.
#+++++++++++++++++++++++++++++++++++++++++++++++++
def actualizarTablas(base):
    global sel_mes
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    cursor = base.cursor()
    i = 0

    for tabla in range(12): # loopeamos entre los 12 meses (los 12 treeview)
        # eliminamos la data existente los treeview
        for item in listatablas[i].get_children():
            listatablas[i].delete(item)

        #traemos nuevamente la data actualizada desde la base de datos del mes en el cual se esté en el bucle, aunque aun no se muestra en el treeview
        traerdata = (f"SELECT * FROM {meses_lc[i]}")
        cursor.execute(traerdata) # ejecutamos el sql
        base.commit() # aplicamos cambios

        rows = cursor.fetchall() # traemos todas las filas
        # finalmente le cargo la data a todas las filas del treeview del mes en el cual esté el bucle para que el usuario las vea
        for row in rows:
            listatablas[i].insert("", "end", values=row)

        i += 1

#+++++++++++++++++++++++++++++++++++++++++++++++++
# actualizarMes - Lanzamos todos los eventos relacionados a los cambios de mes (se lanza cada vez que se presiona un boton de seleccion de mes y al iniciar el programa)
#+++++++++++++++++++++++++++++++++++++++++++++++++
def actualizarMes(mes=1):
        global sel_mes
        global sel_mes_nombre
        
        listameses = [btn_mes1, btn_mes2, btn_mes3, btn_mes4, btn_mes5, btn_mes6, btn_mes7, btn_mes8, btn_mes9, btn_mes10, btn_mes11, btn_mes12]
        listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
        listascrollbars = [scrollbar_1,scrollbar_2,scrollbar_3,scrollbar_4,scrollbar_5,scrollbar_6,scrollbar_7,scrollbar_8,scrollbar_9,scrollbar_10,scrollbar_11,scrollbar_12]
        i = 0; j = 0; k = 0  
        
        # busco los nombres de los botones de meses y les cambio el color por defecto a todos.
        for e in listameses: 
            listameses[i].config(bg=COLOR_BTN_MES, state="normal", cursor="hand2")
            i += 1
        # escondo todas las tablas de meses, luego muestro solo la correspondiente al mes que le pasé a la funcion
        for e in listatablas: 
            listatablas[j].place(x=-1000,y=-1000,width=0,height=0)
            j += 1
        # escondo todas las scrollbars, luego debajo mostramos la correspondiente al mes actual
        for e in listascrollbars:
            listascrollbars[k].place(x=-10, y=-10,width=0,height=0)
            k += 1
        # resalto y deshabilito el boton del mes seleccionado. al indice le resto 1 porque 'mes' es un int que siempre es 1 mayor que el indice de la lista.
        listameses[mes-1].config(bg=COLOR_ACENTO_1, state="disabled", cursor="arrow", disabledforeground="black")
        # ubico en pantalla la tabla que quiero mostrar (la que corresponde al mes que le pasamos a la funcion)
        listatablas[mes-1].place(x=TAB_X, y=TAB_Y, width=TAB_W, height=TAB_H)
         # mostramos la scrollbar que corresponde al treeview que se está viendo
        listascrollbars[mes-1].place(x=1222, y=138,width=16,height=526)

        sel_mes = mes # decimos que la variable global ahora es el mes que le pase a la funcion, para que el resto del codigo sepa en que mes estoy parado
        sel_mes_nombre = meses[mes-1] # aca busco el nombre del mes, en la lista de meses definida al principio, y tmb actualizo la variable global

        actualizarRegistro(f"Se ha cambiado el mes a {sel_mes_nombre}")
        reacomodarColumnas() # reseteo los anchos de las columnas
        actualizarIndicadores()

#+++++++++++++++++++++++++++++++++++++++++++++++++
# botonEnter - Detectamos cuando se presiona el boton de enter. Si estamos en "Alta" o "Editar", enviamos un comando al boton de OK
#+++++++++++++++++++++++++++++++++++++++++++++++++
def botonEnter(event):
    global sel_accion

    if sel_accion == 1:
        RealizarAccion(1)
    elif sel_accion == 2:
        RealizarAccion(2)
#+++++++++++++++++++++++++++++++++++++++++++++++++
# AbrirBarraAcciones - Abrimos el sub-menu de acciones (abmr)
#+++++++++++++++++++++++++++++++++++++++++++++++++
def AbrirBarraAcciones(accion=0):
    global sel_accion
    # mostramos el submenu de acciones
    bar_submenu_parent.place(x=BAR_ACCION_X,y=BAR_ACCION_Y,width=BAR_ACCION_W,height=BAR_ACCION_H)
    # deshabilitamos los botones de acciones para evitar que se puedan acceder utilizando el teclado
    btn_accion_1.config(state="disabled")
    btn_accion_2.config(state="disabled")
    btn_accion_3.config(state="disabled")
    btn_accion_4.config(state="disabled")
    btn_accion_5.config(state="disabled")

    if accion == 1: # Se abre la barra Agregar
        cmp_submenu_agregar_concepto.focus() # ponemos el cursor sobre el campo concepto
        sel_accion = 1
        bar_submenu_agregar_main.place(x=BAR_SUBMENU_X,y=BAR_SUBMENU_Y,width=BAR_SUBMENU_W,height=BAR_SUBMENU_H)
        bar_submenu_editar_main.place(x=0,y=0,width=0,height=0)
    elif accion == 2: # Se abre la barra de Editar
        cmp_submenu_editar_concepto.focus() # ponemos el cursor sobre el campo concepto
        sel_accion = 2
        bar_submenu_agregar_main.place(x=0,y=0,width=0,height=0)
        bar_submenu_editar_main.place(x=BAR_SUBMENU_X,y=BAR_SUBMENU_Y,width=BAR_SUBMENU_W,height=BAR_SUBMENU_H)

#+++++++++++++++++++++++++++++++++++++++++++++++++
# CerrarBarraAcciones - Cerramos el sub-menu de acciones (abmr) y habilitamos los botones nuevamente
#+++++++++++++++++++++++++++++++++++++++++++++++++
def CerrarBarraAcciones():
    global sel_accion
    # ocultamos el submenu de acciones
    bar_submenu_parent.place(x=0,y=0,width=0,height=0)
    #volvemos a habilitar los botones de acciones
    btn_accion_1.config(state="normal")
    btn_accion_2.config(state="normal")
    btn_accion_3.config(state="normal")
    btn_accion_4.config(state="normal")
    btn_accion_5.config(state="normal")

    # si estamos cerrando la barra de accion desde el menu de editar, hacemos algunas instrucciones extras
    if sel_accion == 2:
        habilitarMeses()
        habilitarTablas()
        # escondemos el texto que indica que se está editando en los header de los treeview
        header_editing.place(x=0,y=0,width=0,height=0)
        # cambiamos el texto de edicion al texto de consejo
        txt_maingrid_text.config(text= TEXTO_CONSEJO, anchor= CENTER)

    sel_accion = 0
#+++++++++++++++++++++++++++++++++++++++++++++++++
# RealizarAccion - Accion que se realizará al apretar el boton "OK" en el submenu de acciones
#+++++++++++++++++++++++++++++++++++++++++++++++++
def RealizarAccion(accion):
    if accion == 1: #Dar de alta una operacion, previo validacion de campos mediante regex
        validarCampos("alta")
    elif accion == 2: #Editar una operacion, previo validacion de campos mediante regex
        validarCampos("editar")

#+++++++++++++++++++++++++++++++++++++++++++++++++
# validarCampos - Una vez presionamos el boton "Ok" en alta o en editar, validamos que la info de los campos esté en los formatos requeridos.
#+++++++++++++++++++++++++++++++++++++++++++++++++
def validarCampos(operacion):
    a_concepto = cmp_submenu_agregar_concepto.get()
    a_cantidad = cmp_submenu_agregar_cantidad.get()
    a_costo = cmp_submenu_agregar_costo.get()

    e_concepto = cmp_submenu_editar_concepto.get()
    e_cantidad = cmp_submenu_editar_cantidad.get()
    e_costo = cmp_submenu_editar_costo.get()
    # validamos los campos si la acción fue una nueva alta
    if operacion == "alta":
        # Revisar si los campos estan vacíos
        if not a_cantidad.strip() or not a_costo.strip() or not a_concepto.strip():
            messagebox.showerror("Error en la carga", "Error. Alguno de los campos está vacío.")
        # Revisar si los campos contienen algun caracter no numérico, pero exceptuamos los "puntos" '.'
        elif not re.match(r'^[0-9]*\.?[0-9]*$', a_cantidad) or not re.match(r'^[0-9]*\.?[0-9]*$', a_costo):
            messagebox.showerror("Error en la carga", "Alguno de los campos de 'Cantidad' o 'Costo' poseen caracteres no numéricos. Utilice '.' para separar decimales.")
        else:
            operacion_Alta(a_concepto, a_cantidad, a_costo)
    # validamos los campos si la acción fue editar.
    elif operacion == "editar":
        # Revisar si los campos estan vacíos
        if not e_cantidad.strip() or not e_costo.strip() or not e_concepto.strip():
            messagebox.showerror("Error en la carga", "Error. Alguno de los campos está vacío.")
        # Revisar si los campos contienen algun caracter no numérico, pero exceptuamos los puntos.
        elif not re.match(r'^[0-9]*\.?[0-9]*$', e_cantidad) or not re.match(r'^[0-9]*\.?[0-9]*$', e_costo):
            messagebox.showerror("Error en la carga", "Alguno de los campos de 'Cantidad' o 'Costo' poseen caracteres no numéricos. Utilice '.' para separar decimales.")
        else:
            operacion_Editar_2()
            CerrarBarraAcciones()

#+++++++++++++++++++++++++++++++++++++++++++++++++
# operacion_Alta - Dar de alta una operacion
#+++++++++++++++++++++++++++++++++++++++++++++++++
def operacion_Alta(concepto, cantidad, costo):
    cantidad = float(cantidad)
    costo = float(costo)
    fecha = date.today() # Obtenemos la fecha del momento en que se carga la operacion
    actual = cantidad * costo # calculamos el total de la operacion

    cursor = base.cursor()
    data = (fecha, concepto, cantidad, costo, actual)
    sql = (f"INSERT INTO {meses_lc[sel_mes-1]} ('fecha', 'concepto', 'cantidad', 'precio_u', 'precio_t') VALUES(?, ?, ?, ?, ?)") #INSERT INTO inserta la data dentro de la base de datos (personas en este caso)

    cursor.execute(sql, data) # ejecutamos el sql con la data que le pase
    base.commit() # aplicamos los cambios en la base de datos

    # eliminamos el contenido de los campos de Nueva Operacion
    cmp_submenu_agregar_concepto.delete(0, tk.END)
    cmp_submenu_agregar_cantidad.delete(0, tk.END)
    cmp_submenu_agregar_costo.delete(0, tk.END)
    
    actualizarRegistro(f"Se ha registrado la operación correctamente por un total de: ${actual:.2f}")

    cmp_submenu_agregar_concepto.focus() # ponemos el cursor sobre el campo concepto en agregar, por si el usuario quiere seguir cargando datos.

    actualizarTablas(base)
    actualizarIndicadores()

#+++++++++++++++++++++++++++++++++++++++++++++++++
# operacion_Baja - Dar de baja (eliminar) una operacion
#+++++++++++++++++++++++++++++++++++++++++++++++++
def operacion_Baja():
    global sel_mes_nombre
    global sel_mes

    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    columna_id = 0
    cursor = base.cursor()
    lista_ids = [] # creo la lista que contendrá los ids a eliminar, esta lista se llena en base a las filas seleccionadas
    seleccion = listatablas[sel_mes-1].selection() # obtenemos las filas seleccionadas.
    
    if not seleccion: # si no hay filas seleccionadas, damos un error.
        messagebox.showerror("Error", "Debes seleccionar al menos una fila para eliminarla.")
        return
    else: # si hay filas seleccionadas, procesamos la baja.
        # busco los ids de las filas seleccionadas, realizando una busqueda en la columna de ids.
        for fila in listatablas[sel_mes-1].selection():
            id = int(listatablas[sel_mes-1].item(fila, 'values')[columna_id])
            lista_ids.append(id) # agrego los id encontrados a la lista de ids.

        if len(lista_ids) == 1: # si solo se seleccionó una fila, mostramos el id a eliminar
            respuesta = messagebox.askyesno("Eliminar Operación", (f"¿Deseas eliminar la operación ID #{id}? Su ID único no será reemplazado por registros futuros. Esta acción no se puede deshacer."))
        else: # en cambio si se eliminaron varias, mostramos un mensaje genérico sin hacer enfasis en los ids.
            respuesta = messagebox.askyesno("Eliminar Operaciones", (f"Se han seleccionado 2 o más filas para eliminar. Sus IDs únicos no serán reemplazados por registros futuros. Esta acción no se puede deshacer.\n\n¿Deseas proceder?"))
    
        i = 0
        if respuesta:
            if len(lista_ids) == 1: # si solo seleccionamos una fila
                sql = (f"DELETE FROM {meses_lc[sel_mes-1]} WHERE id = {lista_ids[0]}") # borramos el unico id de la lista
                cursor.execute(sql)
                actualizarRegistro(f"Se ha dado de baja la operación correctamente. ID #{id} eliminado.")
            else: # si seleccionamos varias filas, iterar entre las filas seleccionadas e ir borrandolas.
                for elemento in lista_ids:
                    sql = (f"DELETE FROM {meses_lc[sel_mes-1]} WHERE id = {lista_ids[i]}") # borramos los id presentes en la lista
                    cursor.execute(sql)
                    i += 1
                actualizarRegistro(f"Se han dado de baja las operaciones correctamente.")

            base.commit() #ejecutamos el commit.

            actualizarTablas(base)
            actualizarIndicadores()
            return
        else:
            actualizarRegistro(f"Se ha cancelado el proceso de eliminación.")
            return

#+++++++++++++++++++++++++++++++++++++++++++++++++
# operacion_Editar_1 - Pasos previos a editar una operacion (previo a presionar el botón de "ok")
#+++++++++++++++++++++++++++++++++++++++++++++++++
def operacion_Editar_1():
    global sel_mes_nombre
    global sel_mes
    global edit_id

    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    columna_id = 0
    columna_concepto = 2
    columna_cantidad = 3
    columna_costo = 4
    columna_total = 5
    seleccion = listatablas[sel_mes-1].selection() # obtenemos las filas seleccionadas.
    
    if not seleccion: # si no hay filas seleccionadas, damos un error.
        messagebox.showerror("Error", "Debes seleccionar una fila para editarla.")
        return
    elif len(seleccion) > 1: # si tenemos mas de una fila seleccionada, también mostramos un error.
        messagebox.showerror("Error", "No es posible realizar edición múltiple\nDebes seleccionar una sola fila.")
        return
    else: # si hay solo una fila seleccionada, permitimos editar
        # busco los datos de la fila seleccionada (id, concepto, cantidad, costo y total).
        for fila in listatablas[sel_mes-1].selection():
            id = int(listatablas[sel_mes-1].item(fila, 'values')[columna_id])
            concepto = str(listatablas[sel_mes-1].item(fila, 'values')[columna_concepto])
            cantidad = float(listatablas[sel_mes-1].item(fila, 'values')[columna_cantidad])
            costo = float(listatablas[sel_mes-1].item(fila, 'values')[columna_costo])
            total = float(listatablas[sel_mes-1].item(fila, 'values')[columna_total])

        # posicionamos el texto que indica que se está editando en los header de los treeview
        header_editing.place(x=326,y=142,width=884,height=30)
        # cambiamos el texto de consejo al texto de edición
        txt_maingrid_text.config(text= TEXTO_CONSEJO2, anchor= CENTER)

        # borro cualquier valor que hayan tenido los campos de editar
        cmp_submenu_editar_concepto.delete(0, tk.END)
        cmp_submenu_editar_cantidad.delete(0, tk.END)
        cmp_submenu_editar_costo.delete(0, tk.END)
        # seteo los valores originales a los campos de editar, para que el usuario vea qué está cambiando
        cmp_submenu_editar_concepto.insert(0, concepto)
        cmp_submenu_editar_cantidad.insert(0, cantidad)
        cmp_submenu_editar_costo.insert(0, costo)

        txt_submenu_editar_id.config(text=(f"#{id}"), anchor=W) # mostramos el id que se está editando en la barra de acciones.
        deshabilitarTablas() # deshabilitamos los treeview
        deshabilitarMeses(1) # deshabilitamos los botones de meses y estadisticas
    
        #seteo las variables globales a los valores que retornó la búsqueda en la fila seleccionada, para utilizarlas en la parte 2 de esta funcion.
        edit_id = id

        AbrirBarraAcciones(2) # como se me permitió editar, abro la barra de acciones y muestro los campos para editar.

#+++++++++++++++++++++++++++++++++++++++++++++++++
# operacion_Editar_2 - Pasos posteriores a editar una operacion (posterior a presionar el botón de "ok")
#+++++++++++++++++++++++++++++++++++++++++++++++++
def operacion_Editar_2():
    global edit_id
    # asigno las variables globales a sus correspondientes variables locales, que son las que voy a usar
    id = edit_id
    concepto = str(cmp_submenu_editar_concepto.get())
    cantidad = float(cmp_submenu_editar_cantidad.get())
    costo = float(cmp_submenu_editar_costo.get())
    total = float(cantidad * costo)
    cursor = base.cursor()
                                               
    # importante, debajo por mas que le pasemos un solo parametro, igual tiene que ser una tupla, entonces si es un solo parametro seria, x ej, variable = (parm, )
    data = (concepto, cantidad, costo, total, id) 
    sql = (f"UPDATE {meses_lc[sel_mes-1]} SET concepto=?, cantidad=?, precio_u=?, precio_t=? WHERE id=?") #UPDATE debe respetar el orden de los parametros en data
    cursor.execute(sql, data) # ejecutamos el sql
    base.commit() #aplicamos cambios
    # actualizamos las tablas y los indicadores
    actualizarTablas(base)
    actualizarIndicadores()
    # limpiamos los campos de entrada
    cmp_submenu_editar_concepto.delete(0, tk.END)
    cmp_submenu_editar_cantidad.delete(0, tk.END)
    cmp_submenu_editar_costo.delete(0, tk.END)

    actualizarRegistro(f"Se ha editado la operación ID #{id} correctamente")
    return

#+++++++++++++++++++++++++++++++++++++++++++++++++
# tabla_Reiniciar - Reiniciar el mes actual
#+++++++++++++++++++++++++++++++++++++++++++++++++
def tabla_Reiniciar():
    global sel_mes_nombre
    global sel_mes
    cursor = base.cursor()

    #Validar con el usuario si desea reiniciar el mes actual
    respuesta = messagebox.askyesno("Reiniciar mes", (f"¿Deseas reiniciar la tabla correspondiente al mes de {sel_mes_nombre}? Esta acción no se puede deshacer."))
    if respuesta:
        sql = (f"DELETE FROM {meses_lc[sel_mes-1]}")
        cursor.execute(sql) # ejecutar la base de datos CON la data que le pase
        base.commit() #ejecutamos el commit.

        actualizarTablas(base)
        actualizarIndicadores()
        actualizarRegistro(f"Se ha reiniciado la tabla del mes seleccionado.")
        return
    else:
        actualizarRegistro(f"Has decidido no reiniciar el mes actual.")
        return
#+++++++++++++++++++++++++++++++++++++++++++++++++
# tabla_Formatear - Formatear la base de datos por completo (borra todos los meses)
#+++++++++++++++++++++++++++++++++++++++++++++++++
def tabla_Formatear():
    global sel_mes_nombre
    global sel_mes
    cursor = base.cursor()
    #Validar con el usuario si desea formatear la base de datos
    i = 0
    respuesta = messagebox.askyesno("Formatear base de datos", (f"Atención: Se está por formatear la base de datos.\nPerderás todas las operaciones de todos los meses.\n\nEsta acción no se puede deshacer.\n\n¿Deseas proceder?"))
    if respuesta:
        for tabla in range(12):
            sql = (f"DELETE FROM {meses_lc[i]}")
            cursor.execute(sql) # ejecutar la base de datos CON la data que le pase
            base.commit() #ejecutamos el commit.
            i += 1

        actualizarTablas(base)
        actualizarIndicadores()
        actualizarRegistro(f"Se ha formateado la base de datos. Todas las operaciones han sido eliminadas.")
        return
    else:
        actualizarRegistro(f"Has decidido no formatear la base de datos.")
        return
#---------------------------------------------------------------------------------------------------------------
# VENTANA PRINCIPAL
#---------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("Gestión de Gastos")
root.geometry(VENTANA)
root.config(bg=COLOR_BG)
root.resizable(0,0)
root.maxsize(1280,720)

# asigno el boton de enter a una función que detectará si este se presiona cuando estamos dando de alta o editando una operación.
root.bind('<Return>', botonEnter)

# Inicializamos todas las imagenes que el programa va a usar
im_fondo_hd_init = ImageTk.PhotoImage(Image.open(IM_FONDO_HD)) # (Fondo principal)
im_fondo_st_init = ImageTk.PhotoImage(Image.open(IM_FONDO_ST)) # (Fondo de la barra de estadisticas)

# Imagen de fondo 
im_fondo = Label(root, bg=COLOR_BG, image=im_fondo_hd_init)
im_fondo.place(x=0,y=0,relwidth=1,relheight=1)

# Separadores
sep_1 = Label(root, bg = COLOR_SEP) # sep vertical
sep_1.place(relx=0.246,rely=0.076,relwidth=0.001,relheight=0.91)
sep_2 = Label(root, bg = COLOR_SEP) # sep horizontal
sep_2.place(relx=0.03,rely=0.075,relwidth=0.94,relheight=0.0001)

#-------------------------------------------------
# BARRA DE TITULO
#-------------------------------------------------
# Barra de título
bar_titulo = Label(root, bg = COLOR_ACENTO_1, font=(FUENTE,20), text="CONTROL DE GASTOS", anchor=CENTER)
bar_titulo.place(relx=0.03,rely=0.02,relwidth=0.94,relheight=0.05)

# Texto de version en la barra de titulo
txt_ver = Label(root, bg = COLOR_ACENTO_1, font=(FUENTE_LIGHT,12), text="V 1.0 2023", anchor=W)
txt_ver.place(x=50,rely=0.02,width=80,relheight=0.05)

# Boton de info
btn_info = Button(root, bitmap="info", bg=COLOR_ACENTO_1, command= lambda: MostrarInfo(), cursor="hand2")
btn_info.place(x=1206,rely=0.023,width=30,height=30)

def MostrarInfo():
    messagebox.showinfo("Información", (
        "Control de gastos.\n\nUn gasto es cualquier operación que suponga un costo al usuario.\n\n"
        "Cada operación tiene asociada un gasto total (expresado en moneda corriente) que es el producto entre cantidad y costo unitario.\n\n"
        "Use TAB y ENTER para cargar o editar operaciones más rápido.\n\n"
        "Programa creado por Christian Sánchez - UTN"))

#-------------------------------------------------
# CONTENIDO DE LA BARRA DE SUBTITULO
#-------------------------------------------------
# Barra de subtitulo
bar_subtitulo = Label(root, bg = COLOR_ACENTO_2)
bar_subtitulo.place(relx=0.25,rely=0.082,relwidth=0.72,relheight=0.05)

# Indicador de Mes actual - seteado desde la funcion actualizarIndicadores apenas inicia el programa
bar_mes_actual = Label(bar_subtitulo, bg = COLOR_INDICADORES_BG, fg= COLOR_ACENTO_1, font=(FUENTE,16), text=None, anchor=CENTER)
bar_mes_actual.place(x=0,y=0,width=270,height=32)

# Posiciones de los elementos de la barra de subtitulo (los indicadores)
SUBT_ELEMENTO_X = 328
SUBT_ELEMENTO_W = 140
SUBT_ELEMENTO_SEP = 150

# texto "Gastos"
txt_gastos = Label(bar_subtitulo, bg = COLOR_ACENTO_2, fg= "black", font=(FUENTE_LIGHT,16), text="Total Gastado: ($)", anchor=E)
txt_gastos.place(x=SUBT_ELEMENTO_X + (SUBT_ELEMENTO_SEP * 0),y=0,width=SUBT_ELEMENTO_W,height=32)
# Indicador de Gastos
bar_gastos = Label(bar_subtitulo, bg = COLOR_INDICADORES_BG, fg= "white", font=(FUENTE_LIGHT,16), text="", anchor=CENTER)
bar_gastos.place(x=SUBT_ELEMENTO_X + (SUBT_ELEMENTO_SEP * 1),y=0,width=SUBT_ELEMENTO_W,height=32)
# texto "Cant. de operaciones"
txt_operaciones = Label(bar_subtitulo, bg = COLOR_ACENTO_2, fg= "black", font=(FUENTE_LIGHT,16), text="Operaciones:", anchor=E)
txt_operaciones.place(x=SUBT_ELEMENTO_X + (SUBT_ELEMENTO_SEP * 2),y=0,width=SUBT_ELEMENTO_W,height=32)
# Indicador de Operaciones
bar_operaciones = Label(bar_subtitulo, bg = COLOR_INDICADORES_BG, fg= "white", font=(FUENTE_LIGHT,16), text= "", anchor=CENTER)
bar_operaciones.place(x=SUBT_ELEMENTO_X + (SUBT_ELEMENTO_SEP * 3),y=0,width=SUBT_ELEMENTO_W,height=32)

#-------------------------------------------------
# CONTENIDO DE LA BARRA DE ACCIONES (Inferior a la barra de subtitulo)
#-------------------------------------------------
# Barra de acciones
bar_accion_parent = Label(root, bg = COLOR_BORDE)
bar_accion_parent.place(x=320,y=100,width=922,height=32)

bar_accion_bg = Label(bar_accion_parent, bg = "black", image=im_fondo_st_init)
bar_accion_bg.place(x=0,y=0,width=918,height=28)

BTN_ACCIONES_SEP = 142
BTN_ACCIONES_X = 2
# Boton AGREGAR
btn_accion_1_parent = Label(bar_accion_parent, bg="green")
btn_accion_1_parent.place(x=BTN_ACCIONES_X + BTN_ACCIONES_SEP * 0,y=2,width=138,height=24)
btn_accion_1 = Button(btn_accion_1_parent, command=lambda: AbrirBarraAcciones(1), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 11), text="AGREGAR", bg=COLOR_BG, fg="white", anchor=CENTER, cursor="hand2")
btn_accion_1.place(x=0,y=0,width=134,height=20)
# Boton ELIMINAR
btn_accion_2_parent = Label(bar_accion_parent, bg="red")
btn_accion_2_parent.place(x=BTN_ACCIONES_X + BTN_ACCIONES_SEP * 1,y=2,width=138,height=24)
btn_accion_2 = Button(btn_accion_2_parent, command=lambda: operacion_Baja(), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 11), text="ELIMINAR", bg=COLOR_BG, fg="white", anchor=CENTER, cursor="hand2")
btn_accion_2.place(x=0,y=0,width=134,height=20)
# Boton EDITAR
btn_accion_3_parent = Label(bar_accion_parent, bg="orange")
btn_accion_3_parent.place(x=BTN_ACCIONES_X + BTN_ACCIONES_SEP * 2,y=2,width=138,height=24)
btn_accion_3 = Button(btn_accion_3_parent, command=lambda: operacion_Editar_1(), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 11), text="EDITAR", bg=COLOR_BG, fg="white", anchor=CENTER, cursor="hand2")
btn_accion_3.place(x=0,y=0,width=134,height=20)
# Boton REINICIAR
btn_accion_4_parent = Label(bar_accion_parent, bg="blue")
btn_accion_4_parent.place(x=BTN_ACCIONES_X + BTN_ACCIONES_SEP * 3,y=2,width=138,height=24)
btn_accion_4 = Button(btn_accion_4_parent, command=lambda: tabla_Reiniciar(), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 11), text="REINICIAR", bg=COLOR_BG, fg="white", anchor=CENTER, cursor="hand2")
btn_accion_4.place(x=0,y=0,width=134,height=20)
# Boton REINICIAR TODOS
btn_accion_5_parent = Label(bar_accion_parent, bg="purple")
btn_accion_5_parent.place(x=BTN_ACCIONES_X + BTN_ACCIONES_SEP * 4,y=2,width=138,height=24)
btn_accion_5 = Button(btn_accion_5_parent, command=lambda: tabla_Formatear(), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 11), text="FORMATEAR", bg=COLOR_BG, fg="white", anchor=CENTER, cursor="hand2")
btn_accion_5.place(x=0,y=0,width=134,height=20)

#-------------------------------------------------
# SUBMENU BARRA DE ACCIONES (Aquel que se abre al presionar algun boton de la barra de acciones principal)
#-------------------------------------------------
# Barra de Submenu (Misma posicion que la barra de accion)
BAR_ACCION_X = 320
BAR_ACCION_Y = 100
BAR_ACCION_W = 922
BAR_ACCION_H = 32

BAR_SUBMENU_X = 0
BAR_SUBMENU_Y = 0
BAR_SUBMENU_W = 790
BAR_SUBMENU_H = 28

bar_submenu_parent = Label(root, bg = COLOR_BORDE)
bar_submenu_parent.place(x=0,y=0,width=0,height=0)

bar_submenu_bg = Label(bar_submenu_parent, bg = "black")
bar_submenu_bg.place(x=0,y=0,width=918,height=28)

# a los submenu les asignamos la ubicacion desde AbrirBarraAcciones()
bar_submenu_agregar_main = Label(bar_submenu_parent, bg = "black")

txt_submenu_agregar = Label(bar_submenu_agregar_main, bg = "black", text="AGREGAR: ", font = (FUENTE_LIGHT, 14), fg = "#00FF00", anchor=W)
txt_submenu_agregar.place(x=0,y=-2,width=100,height=24)
txt_submenu_agregar_concepto = Label(bar_submenu_agregar_main, bg = "black", text="CONCEPTO:", font = (FUENTE_LIGHT, 12), fg = "white", anchor=W)
txt_submenu_agregar_concepto.place(x=100,y=0,width=100,height=24)
cmp_submenu_agregar_concepto = Entry(bar_submenu_agregar_main)
cmp_submenu_agregar_concepto.place(x=180,y=0,width=240,height=24)
txt_submenu_agregar_cantidad = Label(bar_submenu_agregar_main, bg = "black", text="CANTIDAD:", font = (FUENTE_LIGHT, 12), fg = "white", anchor=W)
txt_submenu_agregar_cantidad.place(x=450,y=0,width=100,height=24)
cmp_submenu_agregar_cantidad = Entry(bar_submenu_agregar_main)
cmp_submenu_agregar_cantidad.place(x=530,y=0,width=60,height=24)
txt_submenu_agregar_costo = Label(bar_submenu_agregar_main, bg = "black", text="COSTO (UNIT.):", font = (FUENTE_LIGHT, 12), fg = "white", anchor=W)
txt_submenu_agregar_costo.place(x=620,y=0,width=100,height=24)
cmp_submenu_agregar_costo = Entry(bar_submenu_agregar_main)
cmp_submenu_agregar_costo.place(x=720,y=0,width=60,height=24)


    # a los submenu les asignamos la ubicacion desde AbrirBarraAcciones()
bar_submenu_editar_main = Label(bar_submenu_parent, bg = "black")

txt_submenu_editar = Label(bar_submenu_editar_main, bg = "black", text="EDITAR: ", font = (FUENTE_LIGHT, 14), fg = "orange", anchor=W)
txt_submenu_editar.place(x=0,y=-2,width=60,height=24)
txt_submenu_editar_id = Label(bar_submenu_editar_main, bg = "black", text="", font = (FUENTE_LIGHT, 14), fg = "cyan", anchor=W) # num de id que se editará
txt_submenu_editar_id.place(x=70,y=-2,width=100,height=24)
txt_submenu_editar_concepto = Label(bar_submenu_editar_main, bg = "black", text="CONCEPTO:", font = (FUENTE_LIGHT, 12), fg = "white", anchor=W)
txt_submenu_editar_concepto.place(x=160,y=0,width=100,height=24)
cmp_submenu_editar_concepto = Entry(bar_submenu_editar_main)
cmp_submenu_editar_concepto.place(x=230,y=0,width=240,height=24)
txt_submenu_editar_cantidad = Label(bar_submenu_editar_main, bg = "black", text="CANTIDAD:", font = (FUENTE_LIGHT, 12), fg = "white", anchor=W)
txt_submenu_editar_cantidad.place(x=490,y=0,width=100,height=24)
cmp_submenu_editar_cantidad = Entry(bar_submenu_editar_main)
cmp_submenu_editar_cantidad.place(x=560,y=0,width=60,height=24)
txt_submenu_editar_costo = Label(bar_submenu_editar_main, bg = "black", text="COSTO (UNIT.):", font = (FUENTE_LIGHT, 12), fg = "white", anchor=W)
txt_submenu_editar_costo.place(x=640,y=0,width=100,height=24)
cmp_submenu_editar_costo = Entry(bar_submenu_editar_main)
cmp_submenu_editar_costo.place(x=730,y=0,width=60,height=24)

# Botones de OK / ATRAS (Estos son globales y su funcion variará en base al menu que hayamos abierto)
btn_accion_ok = Button(bar_submenu_parent, command=lambda: RealizarAccion(sel_accion), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 12), text="OK", bg="gray", fg="black", cursor="hand2")
btn_accion_ok.place(x=798,y=2,width=58,height=24) # estos botones van a ser invisibles por defecto
btn_accion_cancelar = Button(bar_submenu_parent, command=lambda: CerrarBarraAcciones(), takefocus=False, relief= "flat", overrelief="raised", font=(FUENTE, 12), text="ATRAS", bg="gray", fg="black", cursor="hand2")
btn_accion_cancelar.place(x=858,y=2,width=58,height=24) # estos botones van a ser invisibles por defecto

#-------------------------------------------------
# CONTENIDO DE LA GRILLA PRINCIPAL
#-------------------------------------------------
bg_maingrid_parent = Label(root, bg = COLOR_BORDE)
bg_maingrid_parent.place(x=320,y=136,width=896,height=530)

bg_maingrid_bg = Label(bg_maingrid_parent, bg = COLOR_BG_OSC)
bg_maingrid_bg.place(x=0,y=0,relwidth=1,relheight=1)

# Defino las MACRO globales de las TABLAS
TXT_ID = "ID"
TXT_FECHA = "Fecha"
TXT_CONCEPTO = "Concepto"
TXT_CANTIDAD = "Cantidad"
TXT_COSTO_U = "Costo Unitario"
TXT_COSTO_T = "Costo Total"

COLW_ID = 20
COLW_FECHA = 20
COLW_CONCEPTO = 250
COLW_CANTIDAD = 20
COLW_COSTO_U = 20
COLW_COSTO_T = 20

TAB_X = 2
TAB_Y = 2 
TAB_W = 888
TAB_H = 500

# Configuro el estilo de los treeview (las tablas de meses, aplica para todas)
estilo = ttk.Style(root)
estilo.theme_use("clam") # seteo el tema para los headers, uso clam porque me permite setear el color de fondo de la tabla
estilo.configure("Treeview.Heading", background=COLOR_BG, foreground="white", font=(FUENTE, 12)) # configuro el estilo de los headers de todos los treeview
estilo.configure("Treeview", fieldbackground="gray", background="gray", foreground="black", font=(FUENTE_LIGHT, 12)) # configuro el estilo de todos los treeview (fondo, fuente, etc)

# Treeview de ENERO
tab_mes_1 = ttk.Treeview(bg_maingrid_parent)
tab_mes_1["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de FEBRERO
tab_mes_2 = ttk.Treeview(bg_maingrid_parent)
tab_mes_2["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de MARZO
tab_mes_3 = ttk.Treeview(bg_maingrid_parent)
tab_mes_3["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de ABRIL
tab_mes_4 = ttk.Treeview(bg_maingrid_parent)
tab_mes_4["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de MAYO
tab_mes_5 = ttk.Treeview(bg_maingrid_parent)
tab_mes_5["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de JUNIO
tab_mes_6 = ttk.Treeview(bg_maingrid_parent)
tab_mes_6["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de JULIO
tab_mes_7 = ttk.Treeview(bg_maingrid_parent)
tab_mes_7["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de AGOSTO
tab_mes_8 = ttk.Treeview(bg_maingrid_parent)
tab_mes_8["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de SEPTIEMBRE
tab_mes_9 = ttk.Treeview(bg_maingrid_parent)
tab_mes_9["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de OCTUBRE
tab_mes_10 = ttk.Treeview(bg_maingrid_parent)
tab_mes_10 ["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de NOVIEMBRE
tab_mes_11 = ttk.Treeview(bg_maingrid_parent)
tab_mes_11["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")
# Treeview de DICIEMBRE
tab_mes_12 = ttk.Treeview(bg_maingrid_parent)
tab_mes_12["columns"] = ("col_id", "col_fecha", "col_concepto", "col_cantidad", "col_costo_u", "col_costo_t")

# Header de treeviews
TEXTO_HEADER = ("                ID"
                "                             FECHA"
                "                                                           CONCEPTO"
                "                                                          CANTIDAD"
                "              COSTO UNITARIO"
                "          COSTO TOTAL")
header_bg = Label(root, bg=COLOR_BG, text=TEXTO_HEADER, fg="white", font=(FUENTE_LIGHT, 12), anchor=W)
header_bg.place(x=326,y=142,width=884,height=30)

# Indicador de tabla vacia
TEXTO_VACIA = "                                             LA TABLA ESTÁ VACÍA"
header_vacia = Label(root, bg="gray", text=TEXTO_VACIA, fg=COLOR_GRIS_OSC, font=(FUENTE_LIGHT, 24), anchor = W)
header_vacia.place(x=0,y=0,width=0,height=0) # (x=330,y=342,width=876,height=100)

GRILLA_SEP_X = 326
GRILLA_SEP_ESP = 108

# Separadores de los treeview
grilla_sep_1 = Label(root, bg = COLOR_BG_OSC) # sep vertical
grilla_sep_1.place(x=GRILLA_SEP_X + (GRILLA_SEP_ESP * 1),y=142,width=1,height=496)
grilla_sep_2 = Label(root, bg = COLOR_BG_OSC) # sep vertical
grilla_sep_2.place(x=GRILLA_SEP_X + (GRILLA_SEP_ESP * 2) + 2,y=142,width=1,height=496)
grilla_sep_3 = Label(root, bg = COLOR_BG_OSC) # sep vertical
grilla_sep_3.place(x=GRILLA_SEP_X + (GRILLA_SEP_ESP * 5) + 16,y=142,width=1,height=496)
grilla_sep_4 = Label(root, bg = COLOR_BG_OSC) # sep vertical
grilla_sep_4.place(x=GRILLA_SEP_X + (GRILLA_SEP_ESP * 6) + 17,y=142,width=1,height=496)
grilla_sep_5 = Label(root, bg = COLOR_BG_OSC) # sep vertical
grilla_sep_5.place(x=GRILLA_SEP_X + (GRILLA_SEP_ESP * 7) + 18,y=142,width=1,height=496)

# Header de treeviews cuando se está editando
TEXTO_EDITANDO = "↑↑↑   Por favor, ingrese el nuevo Concepto, Cantidad y Costo de la operación a editar.   ↑↑↑"
header_editing = Label(root, bg=COLOR_BG_OSC, text=TEXTO_EDITANDO, fg="orange", font=(FUENTE_LIGHT, 12))
header_editing.place(x=0,y=0,w=0,h=0) #(x=326,y=142,width=884,height=30)



# Fondo de las scrollbar
scrollbar_fondo = Label(root, bg=COLOR_BORDE)
scrollbar_fondo.place(x=1220, y=136,width=20,height=530)
# Creamos una barra de desplazamiento para cada treeview
scrollbar_1 = Scrollbar(root, orient="vertical", command=tab_mes_1.yview)
scrollbar_2 = Scrollbar(root, orient="vertical", command=tab_mes_2.yview)
scrollbar_3 = Scrollbar(root, orient="vertical", command=tab_mes_3.yview)
scrollbar_4 = Scrollbar(root, orient="vertical", command=tab_mes_4.yview)
scrollbar_5 = Scrollbar(root, orient="vertical", command=tab_mes_5.yview)
scrollbar_6 = Scrollbar(root, orient="vertical", command=tab_mes_6.yview)
scrollbar_7 = Scrollbar(root, orient="vertical", command=tab_mes_7.yview)
scrollbar_8 = Scrollbar(root, orient="vertical", command=tab_mes_8.yview)
scrollbar_9 = Scrollbar(root, orient="vertical", command=tab_mes_9.yview)
scrollbar_10= Scrollbar(root, orient="vertical", command=tab_mes_10.yview)
scrollbar_11= Scrollbar(root, orient="vertical", command=tab_mes_11.yview)
scrollbar_12= Scrollbar(root, orient="vertical", command=tab_mes_12.yview)

def AsignarScrollbars():
    listatablas = [tab_mes_1, tab_mes_2, tab_mes_3, tab_mes_4, tab_mes_5, tab_mes_6, tab_mes_7, tab_mes_8, tab_mes_9, tab_mes_10, tab_mes_11, tab_mes_12]
    listascrollbars = [scrollbar_1,scrollbar_2,scrollbar_3,scrollbar_4,scrollbar_5,scrollbar_6,scrollbar_7,scrollbar_8,scrollbar_9,scrollbar_10,scrollbar_11,scrollbar_12]
    i = 0
    for tabla in listatablas:
        # le asignamos la barra de desplazamiento a su treeview correspondiente, iterando entre los treeview
        listatablas[i].configure(yscrollcommand=listascrollbars[i].set)
        i += 1

#-------------------------------------------------
# PANEL INFERIOR (Registro de actividades)
#-------------------------------------------------
bg_registro_parent = Label(root, bg = COLOR_BORDE)
bg_registro_parent.place(x=320,y=670,width=922,height=32)
bg_registro_bg = Label(bg_registro_parent, bg = COLOR_BG_OSC)
bg_registro_bg.place(x=0,y=0,relwidth=1,relheight=1)
bg_registro = Label(bg_registro_bg, bg = COLOR_BG_OSC, text= "El registro de actividad se encuentra vacío", fg= "darkgray", font=(FUENTE_LIGHT, 12), anchor=W)
bg_registro.place(x=0,y=0,relwidth=1,relheight=1)

TEXTO_CONSEJO = "Mantener presionado 'CTRL' para selección múltiple."
TEXTO_CONSEJO2 = "Tablas y selección de meses deshabilitadas mientras se esté editando una operación."
# marco (fondo) del texto de consejo
txt_maingrid_text_bg = Label(root, bg = "cyan")
txt_maingrid_text_bg.place(x=324,y=642,width=888,height=20)
# texto de consejo
txt_maingrid_text = Label(txt_maingrid_text_bg, fg= "gray", bg = COLOR_BG_OSC, text= TEXTO_CONSEJO, anchor= CENTER)
txt_maingrid_text.place(x=0,y=-2,width=884,height=20)

#-------------------------------------------------
# PANEL IZQUIERDO
#-------------------------------------------------

#Cuadrado de "Año"
bg_año_parent = Label(root, bg = COLOR_BORDE)
bg_año_parent.place(x=38,y=58,width=274,height=78)

bg_año_bg = Label(bg_año_parent, bg = COLOR_BG)
bg_año_bg.place(x=0,y=0,relwidth=1,relheight=1)

bg_año_text = Label(bg_año_parent, bg = "black", fg= COLOR_ACENTO_1, font=(FUENTE, 16), text="AÑO:", anchor=CENTER)
bg_año_text.place(x=4,y=2,width=262,height=30)

# Indicador de año
btn_año1 = Label(bg_año_parent, font=(FUENTE, 16), text="2023", bg="gray", fg="black")
btn_año1.place(x=4,y=38,width=262,height=30)

#Cuadrado de "Meses"
bg_meses_parent = Label(root, bg = COLOR_BORDE)
bg_meses_parent.place(x=38,y=140,width=274,height=494)

bg_meses_bg = Label(bg_meses_parent, bg = COLOR_BG)
bg_meses_bg.place(x=0,y=0,relwidth=1,relheight=1)

bg_meses_text = Label(bg_meses_parent, bg = "black", fg= COLOR_ACENTO_1, font=(FUENTE, 16), text="MES:", anchor=CENTER)
bg_meses_text.place(x=4,y=2,width=262,height=30)

#defino los tamaños y separacion de los botones de los meses
btn_mes_x = 4
btn_mes_y = 38
btn_mes_w = 262
btn_mes_h = 30
btn_mes_sep = 38
# botones de Meses
btn_mes1 = Button(bg_meses_parent, takefocus=False, text="ENERO", command=lambda: actualizarMes(1), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes2 = Button(bg_meses_parent, takefocus=False, text="FEBRERO", command=lambda: actualizarMes(2), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes3 = Button(bg_meses_parent, takefocus=False, text="MARZO", command=lambda: actualizarMes(3), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes4 = Button(bg_meses_parent, takefocus=False, text="ABRIL", command=lambda: actualizarMes(4), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes5 = Button(bg_meses_parent, takefocus=False, text="MAYO", command=lambda: actualizarMes(5), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes6 = Button(bg_meses_parent, takefocus=False, text="JUNIO", command=lambda: actualizarMes(6), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes7 = Button(bg_meses_parent, takefocus=False, text="JULIO", command=lambda: actualizarMes(7), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes8 = Button(bg_meses_parent, takefocus=False, text="AGOSTO", command=lambda: actualizarMes(8), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes9 = Button(bg_meses_parent, takefocus=False, text="SEPTIEMBRE", command=lambda: actualizarMes(9), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes10 = Button(bg_meses_parent, takefocus=False, text="OCTUBRE", command=lambda: actualizarMes(10), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes11 = Button(bg_meses_parent, takefocus=False, text="NOVIEMBRE", command=lambda: actualizarMes(11), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")
btn_mes12 = Button(bg_meses_parent, takefocus=False, text="DICIEMBRE", command=lambda: actualizarMes(12), relief= "flat", overrelief="raised", font=(FUENTE, 16), bg=COLOR_BTN_MES, fg="black", cursor="hand2")

def ubicarBotonesMeses():
    listameses = [btn_mes1, btn_mes2, btn_mes3, btn_mes4, btn_mes5, btn_mes6, btn_mes7, btn_mes8, btn_mes9, btn_mes10, btn_mes11, btn_mes12]
    i = 0
    for mes in listameses:
        listameses[i].place(x=btn_mes_x,y=btn_mes_y + (btn_mes_sep * i) ,width=btn_mes_w,height=btn_mes_h)
        i += 1
ubicarBotonesMeses()

# Boton de Estadísticas
boton_estadisticas_bg = Label(root, bg = "black" )
boton_estadisticas_bg.place(x=42,y=648,width=266,height=40)
boton_estadisticas = Button(boton_estadisticas_bg, takefocus=False, command = lambda: MostrarEstadisticas(sel_estadisticas), bg = "cyan", text="ESTADÍSTICAS", font=(FUENTE, 14), fg="black", anchor=CENTER, cursor="hand2", relief="flat", overrelief="ridge" )
boton_estadisticas.place(x=1,y=1,width=260,height=34)

#-------------------------------------------------
# ESTADÍSTICAS
#-------------------------------------------------

# definiciones de barras de series de los cuadros
ST_CUADRO_BAR_X = 0
ST_CUADRO_BAR_SEP = 71
ST_CUADRO_BAR_W = 40
ST_CUADRO_BAR_COLOR_1 = "cyan" # color de las barras del cuadro Gastos
ST_CUADRO_BAR_COLOR_2 = "orange" # color de las barras del cuadro Operaciones
# definiciones de nombres de barras (meses)
ST_CUADRO_TXT_X = 68
ST_CUADRO_TXT_Y = 484
ST_CUADRO_TXT_W = 40
ST_CUADRO_TXT_H = 22
ST_CUADRO_TXT_SEP = 71 # separacion entre nombres de los meses
ST_CUADRO_TXT_COLOR_1 = "orange" # color de la leyenda del cuadro Gastos
ST_CUADRO_TXT_COLOR_2 = "cyan" # color de la leyenda del cuadro Operaciones
# definiciones de posicion (cantidades de barras de gastos)
ST_CUADRO_TXT_QTY_X = 54
ST_CUADRO_TXT_QTY_W = 70
ST_CUADRO_TXT_QTY_SEP = 71
# separadores de los cuadros
CUADRO_SEP_Y = 130
CUADRO_SEP = 105

# Ventana principal de estadisticas, contiene todos los demas elementos
bg_estadisticas_parent = Label(root, bg = COLOR_BORDE)

# Ventana principal de estadisticas, da el color de fondo
bg_estadisticas_bg = Label(bg_estadisticas_parent, bg = COLOR_BG)
bg_estadisticas_bg.place(x=0,y=0,relwidth=1,relheight=1)

#Imagen de fondo
im_fondo = Label(bg_estadisticas_parent, image=im_fondo_st_init)
im_fondo.place(x=4,y=30,width=910,height=40)

# Barra de titulo de estadisticas
bar_titulo_st = Label(bg_estadisticas_parent, bg = COLOR_BG_OSC, text="E S T A D Í S T I C A S", fg="white", font=(FUENTE, 16))
bar_titulo_st.place(relx=0,rely=0,relwidth=1,relheight=0.055)

# Boton de cerrar Estadisticas
btn_estadisticas_salir = Button(bar_titulo_st, command= lambda: CerrarEstadisticas(), bg = COLOR_BTN_MES, text="X", takefocus=False, font=("", 14, "bold"), fg="black", anchor=CENTER, cursor="hand2", relief="flat", overrelief="ridge")
btn_estadisticas_salir.place(x=886,y=2,width=26,height=26)

# Botones de seleccion (Gastos / Operaciones)
btn_estadisticas_gto = Button(bg_estadisticas_parent, command= lambda: MostrarEstadisticas(0), takefocus=False, bg = COLOR_BTN_MES, text="GASTOS ($)", font=(FUENTE, 12), disabledforeground= "black", fg="black", anchor=CENTER, cursor="hand2", relief="flat", overrelief="ridge")
btn_estadisticas_gto.place(x=6,y=36,width=150,height=30)
btn_estadisticas_ops = Button(bg_estadisticas_parent, command= lambda: MostrarEstadisticas(1), takefocus=False, bg = COLOR_BTN_MES, text="OPERACIONES", font=(FUENTE, 12), disabledforeground= "black", fg="black", anchor=CENTER, cursor="hand2", relief="flat", overrelief="ridge")
btn_estadisticas_ops.place(x=162,y=36,width=150,height=30)

    #---------------------------
    # GASTOS
    #---------------------------
# Ventana de GASTOS (La ventana la posicionamos desde MostrarEstadisticas()
bg_estadisticas_gto_parent = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC)

# Borde del cuadro de gastos (el que da el color del borde gris)
bg_estadisticas_gto_cuadro_bg = Label(bg_estadisticas_gto_parent, bg = COLOR_GRIS_OSC) 
bg_estadisticas_gto_cuadro_bg.place(x=64,y=34,relwidth=0.92,relheight=0.85)
# Fondo del cuadro de gastos
bg_estadisticas_gto_cuadro = Label(bg_estadisticas_gto_cuadro_bg, bg = "black")
bg_estadisticas_gto_cuadro.place(x=0,y=0,relwidth=1,relheight=1)
# Cuadro de gastos como tal (el que contiene las barras)
bg_estadisticas_gastos = Label(bg_estadisticas_gto_cuadro, bg = "black")
bg_estadisticas_gastos.place(x=0,y=20,relwidth=1,relheight=0.955)

# Barra de titulo de Gastos
bar_gto_titulo_st = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, text="G A S T O S", fg="orange", font=(FUENTE, 16))
bar_gto_titulo_st.place(x=0,y=2,relwidth=1,relheight=0.055)

# Aviso de "sin operaciones cargadas" (cuadro gastos)
bg_estadisticas_gto_adv = Label(bg_estadisticas_gto_cuadro_bg, bg = "black", text="NO HAY OPERACIONES\nCARGADAS", font=(FUENTE_LIGHT, 28), fg=COLOR_GRIS_OSC )

# Separadores del cuadro Gastos
bg_estadisticas_gto_sep1 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 1 (100%)
bg_estadisticas_gto_sep2 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 2 (75%)
bg_estadisticas_gto_sep3 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 3 (50%)
bg_estadisticas_gto_sep4 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 4 (25%)

# Barras de series de gastos
bg_st_gto_1 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_2 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_3 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_4 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_5 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_6 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_7 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_8 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_9 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_10 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_11 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
bg_st_gto_12 = Label(bg_estadisticas_gastos, bg = ST_CUADRO_BAR_COLOR_1)
# Nombres de los meses en Gastos
txt_st_gto_mes_1 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="ENE", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_2 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="FEB", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_3 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="MAR", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_4 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="ABR", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_5 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="MAY", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_6 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="JUN", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_7 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="JUL", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_8 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="AGO", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_9 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="SEP", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_10 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="OCT", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_11 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="NOV", font=(FUENTE_LIGHT, 12))
txt_st_gto_mes_12 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="DIC", font=(FUENTE_LIGHT, 12))
# Cantidades de gastos (bajo el cuadro, por mes) en Gastos / El texto es seteado desde MostrarEstadisticas
txt_st_gto_qty_1 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_2 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_3 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_4 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_5 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_6 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_7 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_8 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_9 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_10 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_11 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_12 = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
# Cantidades de gastos en los separadores del cuadro
txt_st_gto_qty_1a = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_2a = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_3a = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_4a = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="", font=(FUENTE_LIGHT, 12))
# Porcentajes de gastos en los separadores del cuadro
txt_st_gto_qty_1b = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="100%", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_2b = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="75%", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_3b = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="50%", font=(FUENTE_LIGHT, 12))
txt_st_gto_qty_4b = Label(bg_estadisticas_gto_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_1, text="25%", font=(FUENTE_LIGHT, 12))

    #---------------------------
    # OPERACIONES
    #---------------------------
# Ventana de OPERACIONES (La ventana la posicionamos desde MostrarEstadisticas()
bg_estadisticas_ops_parent = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC)

# Borde del cuadro de operaciones (el que da el color del borde gris)
bg_estadisticas_ops_cuadro_bg = Label(bg_estadisticas_ops_parent, bg = COLOR_GRIS_OSC) 
bg_estadisticas_ops_cuadro_bg.place(x=64,y=34,relwidth=0.92,relheight=0.85)
# Fondo del cuadro de operaciones
bg_estadisticas_ops_cuadro = Label(bg_estadisticas_ops_cuadro_bg, bg = "black")
bg_estadisticas_ops_cuadro.place(x=0,y=0,relwidth=1,relheight=1)
# Cuadro de operaciones como tal (el que contiene las barras)
bg_estadisticas_operaciones = Label(bg_estadisticas_ops_cuadro, bg = "black")
bg_estadisticas_operaciones.place(x=0,y=20,relwidth=1,relheight=0.955)

# Barra de titulo de operaciones
bar_ops_titulo_st = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, text="O P E R A C I O N E S", fg="cyan", font=(FUENTE, 16))
bar_ops_titulo_st.place(x=0,y=2,relwidth=1,relheight=0.055)

# Aviso de "sin operaciones cargadas" (cuadro operaciones)
bg_estadisticas_ops_adv = Label(bg_estadisticas_ops_cuadro_bg, bg = "black", text="NO HAY OPERACIONES\nCARGADAS", font=(FUENTE_LIGHT, 28), fg=COLOR_GRIS_OSC )

# Separadores del cuadro Operaciones
bg_estadisticas_ops_sep1 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 1 (100%)
bg_estadisticas_ops_sep2 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 2 (75%)
bg_estadisticas_ops_sep3 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 3 (50%)
bg_estadisticas_ops_sep4 = Label(bg_estadisticas_bg, bg = COLOR_BG_OSC) # separador 4 (25%)

# Barras de series de operaciones
bg_st_ops_1 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_2 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_3 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_4 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_5 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_6 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_7 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_8 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_9 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_10 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_11 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
bg_st_ops_12 = Label(bg_estadisticas_operaciones, bg = ST_CUADRO_BAR_COLOR_2)
# Nombres de los meses en Operaciones
txt_st_ops_mes_1 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="ENE", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_2 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="FEB", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_3 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="MAR", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_4 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="ABR", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_5 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="MAY", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_6 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="JUN", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_7 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="JUL", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_8 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="AGO", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_9 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="SEP", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_10 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="OCT", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_11 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="NOV", font=(FUENTE_LIGHT, 12))
txt_st_ops_mes_12 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="DIC", font=(FUENTE_LIGHT, 12))
# Cantidades de gastos (bajo el cuadro, por mes) en Operaciones / El texto es seteado desde MostrarEstadisticas
txt_st_ops_qty_1 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_2 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_3 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_4 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_5 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_6 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_7 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_8 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_9 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_10 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_11 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_12 = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
# Cantidades de operaciones en los separadores del cuadro
txt_st_ops_qty_1a = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_2a = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_3a = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_4a = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="", font=(FUENTE_LIGHT, 12))
# Porcentajes de operaciones en los separadores del cuadro
txt_st_ops_qty_1b = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="100%", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_2b = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="75%", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_3b = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="50%", font=(FUENTE_LIGHT, 12))
txt_st_ops_qty_4b = Label(bg_estadisticas_ops_parent, bg = COLOR_BG_OSC, fg=ST_CUADRO_TXT_COLOR_2, text="25%", font=(FUENTE_LIGHT, 12))

#-------------------------------------------------
# PROCESOS PRINCIPALES 
#-------------------------------------------------
AsignarScrollbars() # Asignamos los scrollbars a cada tabla.
reacomodarColumnas() #Le damos los valores y anchos por defecto a todas las columnas de todos los treeview. 
ObtenerMesActual() # primero obtengo el mes actual para seleccionar el boton correspondiente ni bien inicia el programa
actualizarMes(sel_mes) # corremos la funcion para que por defecto muestre el mes actual al iniciar
base = crearBase() # creo la conección con la base de datos, o la utilizo si ya existe
checkTablas(base) #checkeo si las tablas en "base" (la base de datos) ya existen, o sino las creo.
actualizarRegistro("El programa ha iniciado correctamente y se ha seleccionado el mes actual.")
actualizarIndicadores() # muestro los indicadores reales del mes que estemos mostrando.

root.mainloop()

# Creado por Christian Sánchez para Curso de nivel inicial UTN
# Prof. Juan Barreto