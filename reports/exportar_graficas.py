import streamlit as st

def crear_reporte():
    st.success("Reporte generado exitosamente.")

def main(df):
    st.button("Generar Reporte",on_click=crear_reporte())