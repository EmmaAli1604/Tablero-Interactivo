import pandas as pd
import streamlit as st
import plotly.express as px
from data.loader import cargar_excel, exportar_excel, exportar_pdf
from reports.creacion_tablas import crear_tabla
from filtrers.filtros import filtros
import uuid
import time
from config.rutas import EXPORT_PATH
import os

#Configuracion de la pagina

st.set_page_config(
    page_title="Tablero Interactivo",
    page_icon="📋",
    layout = "wide",  
)

#Titulo de la pagina
st.title("Construcciones en 2025")
st.markdown("### Edificaciones que se construyeron en el año 2025 y sus datos respectivamente")

#Introduccion

with st.expander("Introduccón",True):
    st.markdown(
        """ 
            * **Esto es una prueba para poder generar tablas** 
            * **reporte**
            * **visualizar datos**
        """
    )
    

#Normalizar
#df['respuesta'] = df['respuesta'].apply(
    #lambda x: 'SI' if str(x).strip().lower() in ['sí', 'si', 's'] 
    #else 'NO' if str(x).strip().lower() in ['no', 'n'] 
    #else x
#)

df = cargar_excel()
st.header("Datos del DataFrame")
st.dataframe(df)
now = time.strftime("%Y%m%d_%H%M%S")
st.button("Exportar en Excel", on_click=exportar_excel, args=(df,EXPORT_PATH +  f"reporte_{now}.xlsx"))
st.button("Exportar en PDF", on_click=exportar_pdf, args=(df,EXPORT_PATH + f"reporte_{now}.pdf"))

st.header("Filtro de datos")
df_filtrer = filtros(df)

col1, col2, col3 = st.columns([3, 3, 3])

with col2:
    st.markdown("<h4 style='font-size:22px;'>¿Deseas graficar los datos filtrados?</h4>", unsafe_allow_html=True)
    op_filtrar = st.radio("", ("No","Si"))

# Si el usuario decide filtrar los datos, se actualiza el DataFrame
if op_filtrar == "Si":
    df = df_filtrer
    
key_prefix = f"grafico_{uuid.uuid4()}"

st.header("Creación de tablas")
crear_tabla(df,key_suffix = "tabla_principal")

st.header("Resumén general de los datos")
resumen = df.describe()
st.dataframe(resumen)
