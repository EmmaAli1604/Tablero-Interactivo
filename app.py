import pandas as pd
import streamlit as st
import plotly.express as px
from data.loader import cargar_excel
from reports.creacion_tablas import crear_tabla
from filtrers.filtros import filtros
from reports.crear_reporte import main as crear_reporte
import uuid

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
    

df = cargar_excel()
st.header("Datos del DataFrame")
st.dataframe(df)

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

st.header ("Creación de reporte")
crear_reporte(df)
