import streamlit as st
import plotly.express as px
import pandas as pd
import time
from data.loader import exportar_excel,exportar_pdf

from config.rutas import EXPORT_PATH
from data.loader import exportar_excel

def checar_previsualizacion(df_filtrado, df, columnas):
    if not df_filtrado.equals(df):
        if columnas:
            st.dataframe(df_filtrado[columnas])
            return(df_filtrado[columnas])
        else:
            st.dataframe(df_filtrado)
            return(df_filtrado)
    else:
        st.warning("No se encontraron datos con los filtros aplicados.")
        
def filtros(df):
    with st.expander("Filtrar datos", True):
        
        df_filtrado = df.copy()
        
        opciones_estado = ["Sin estado"] + sorted(list(df["State"].dropna().unique()))
        opciones_fecha = ["Sin Fecha"] + sorted(list(df["Construction Date"].dropna().unique()),reverse=True)
        
        columnas = st.multiselect("Selecciona las columnas a filtrar:", df.columns)
        
        columna_buscar = st.selectbox("Selecciona la columna para buscar una palabra:",["Sin columna"] + df.columns.tolist())
        
        palabra_buscar = st.text_input("🔍 Ingresa la palabra a buscar: ")
        
        col1, col2 , col3 = st.columns(3)
        
        with col1:
            estado_seleccionado = st.selectbox("Estado:", opciones_estado)

        with col2:
            fecha_seleccionada = st.selectbox("Fecha:", opciones_fecha)
            
        with col3:
            o_l = st.radio("Escoger opción:",["Sin opción"] + df["Owned or Leased"].dropna().unique().tolist())
        
        col4, col5 = st.columns(2)
        
        with col4:
            building_status = st.selectbox("Estado del edificio:",  ["Sin estado"] + df["Building Status"].dropna().unique().tolist())
        with col5:
            real_asset_type = st.selectbox("Tipo de activo real:", ["Sin tipo"] + df["Real Property Asset Type"].dropna().unique().tolist())

        if estado_seleccionado != "Sin estado":
            df_filtrado = df_filtrado[df_filtrado["State"] == estado_seleccionado]

        if fecha_seleccionada != "Sin Fecha":
            df_filtrado = df[df["Construction Date"] == int(fecha_seleccionada)]

        if o_l != "Sin opción":
            df_filtrado = df_filtrado[df_filtrado["Owned or Leased"] == o_l]

        if building_status != "Sin estado":
            df_filtrado = df_filtrado[df_filtrado["Building Status"] == building_status]

        if real_asset_type != "Sin tipo":
            df_filtrado = df_filtrado[df_filtrado["Real Property Asset Type"] == real_asset_type]

        # Filtro por búsqueda
        if columna_buscar != "Sin columna" and palabra_buscar:
            mascara = df_filtrado[columna_buscar].astype(str).str.contains(palabra_buscar, case=False, na=False)
            df_filtrado = df_filtrado[mascara]
            st.success(f"Se encontraron {mascara.sum()} coincidencias para '{palabra_buscar}' en la columna '{columna_buscar}'.")

        # Mostrar resultado
        st.markdown("### Resultado del filtrado")

        df_filtrado =checar_previsualizacion(df_filtrado, df, columnas)
        
        now = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"reporte_{now}.xlsx"
        st.button("Exportar en Excel de datos filtrados", on_click=exportar_excel, args=(df_filtrado,EXPORT_PATH + file_name))
        st.button("Exportar en PDF de datos filtrados", on_click=exportar_pdf, args=(df_filtrado,EXPORT_PATH + f"reporte_{now}.pdf"))

        return df_filtrado
    
#####

def filtros(df):
    with st.expander("Filtrar datos", True):
        df_filtrado = df.copy()

        # 🧼 Asegúrate de que 'Construction Date' sea datetime
        df_filtrado["Construction Date"] = pd.to_datetime(df_filtrado["Construction Date"], errors="coerce")

        # 📆 Filtro por rango de fechas
        st.markdown("### 📅 Filtrar por rango de fechas de construcción")
        min_fecha = df_filtrado["Construction Date"].min().date()
        max_fecha = df_filtrado["Construction Date"].max().date()

        col_fecha1, col_fecha2 = st.columns(2)
        with col_fecha1:
            fecha_inicio = st.date_input("Desde:", value=min_fecha, min_value=min_fecha, max_value=max_fecha)
        with col_fecha2:
            fecha_fin = st.date_input("Hasta:", value=max_fecha, min_value=min_fecha, max_value=max_fecha)

        return df_filtrado


import re

texto = """
Inversión total: $120.000
Presupuesto aprobado: 20 mdp
Costo estimado: USD 3,500.00
Monto alterno: 15 mil
"""

# Regex que detecta valores monetarios comunes
patron = r"""
(?i)                # ignorar mayúsculas/minúsculas
(?:\$|usd\s?)?      # símbolo $ o "usd" opcional
\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?   # número como 120.000 o 3,500.00
(?:\s?(mil|millones|mdp|k|m))?     # sufijo como mil, mdp, millones (opcional)
"""

coincidencias = re.findall(patron, texto, flags=re.VERBOSE)

# re.findall devolverá los grupos si usas paréntesis: para obtener el texto completo, usa re.finditer
matches = re.finditer(patron, texto, flags=re.VERBOSE)
for m in matches:
    print(m.group())
