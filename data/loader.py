import pandas as pd
import streamlit as st
from config.rutas import EXCEL_PATH

def cargar_excel():
    try:
        prog_df = pd.read_excel(EXCEL_PATH)
        st.success("Datos cargados exitosamente")
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
    return prog_df