import streamlit as st

def crear_reporte():
    st.success("Reporte generado exitosamente.")

def main(df):
    st.subheader("Portada del Reporte")
    st.subheader("")
    st.button("Generar Reporte",on_click=crear_reporte())