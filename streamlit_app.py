"""
git add . && git commit -m "" && git push
"""
# Importación de bibliotecas
import pandas as pd
import plotly.express as px
import numpy as np
import sklearn as sk
import streamlit as st
from datetime import datetime

# Carga de datos
df_aprobado = pd.read_json('datasets/Reporte_Proyecto_APROBADO.json')
df_desaprobado = pd.read_json('datasets/Reporte_Proyecto_DESAPROBADO.json')
df_evaluacion = pd.read_json('datasets/Reporte_Proyecto_EN EVALUACION.json')

# Transformacion del formato de fechas
df_aprobado['FECHA_INICIO'] = df_aprobado['FECHA_INICIO'].astype('datetime64[ns]')
df_desaprobado['FECHA_INICIO'] = df_desaprobado['FECHA_INICIO'].astype('datetime64[ns]')
df_evaluacion['FECHA_INICIO'] = df_evaluacion['FECHA_INICIO'].astype('datetime64[ns]')

df_aprobado['AÑO'] = df_aprobado['FECHA_INICIO'].apply(lambda time: time.year)
df_aprobado['MES'] = df_aprobado['FECHA_INICIO'].apply(lambda time: time.month)
df_aprobado['DIA'] = df_aprobado['FECHA_INICIO'].apply(lambda time: time.day)

df_desaprobado['AÑO'] = df_desaprobado['FECHA_INICIO'].apply(lambda time: time.year)
df_desaprobado['MES'] = df_desaprobado['FECHA_INICIO'].apply(lambda time: time.month)
df_desaprobado['DIA'] = df_desaprobado['FECHA_INICIO'].apply(lambda time: time.day)

df_evaluacion['AÑO'] = df_evaluacion['FECHA_INICIO'].apply(lambda time: time.year)
df_evaluacion['MES'] = df_evaluacion['FECHA_INICIO'].apply(lambda time: time.month)
df_evaluacion['DIA'] = df_evaluacion['FECHA_INICIO'].apply(lambda time: time.day)

# Swap de latitud y longitud mal ingresadas (No hay proyecto en el antártida, por debajo de latitud -74)
df_aprobado['LATITUD'],df_aprobado['LONGITUD']=np.where(df_aprobado['LATITUD']<-74,(df_aprobado['LONGITUD'],df_aprobado['LATITUD']),(df_aprobado['LATITUD'],df_aprobado['LONGITUD']))

# Unificación de datas para visualización (aprobados y desaprobados)
df_unificado =  pd.concat([df_aprobado, df_desaprobado])


#App
st.title('Certificación Ambiental - Proyecto Final')

st.write('Bienvenidx al **app**')
st.write()

#Proyectos con fecha
st.write('Proyectos por fecha')
fecha_inicio = st.slider("Ver informacion registrada en:",
    value = datetime(2020,1,1,9,30),
    format = "DD/MM/YY - hh:mm")
st.write("Fecha seleccionada:", fecha_inicio)

#Visualizar datos de dataset
opcion_dataset = st.selectbox(
     '¿Qué dataset deseas visualizar?',
     ('Proyectos aprobados', 'Proyectos desaprobados', 'Proyectos en evaluacion'))
df_visualizacion = None
estado = '-'
if opcion_dataset == 'Proyectos aprobados':
    df_visualizacion = df_aprobado
    estado = 'aprobados'
elif opcion_dataset == 'Proyectos desaprobados':
    df_visualizacion = df_desaprobado
    estado = 'desaprobados'
elif opcion_dataset == 'Proyectos en evaluacion':
    df_visualizacion = df_evaluacion
    estado = 'en evaluación'

st.write('Seleccionó ', len(df_visualizacion.index),'proyectos',estado,'para visualizar:')

st.write('Tabla de datos',estado,'en formato DataFrame')
st.table(df_visualizacion)

st.write('Ubicación de los proyectos',estado)
df_visualizacion = df_visualizacion.rename(columns={'LATITUD':'lat', 'LONGITUD':'lon'})
st.map(df_visualizacion[['lat','lon']])

