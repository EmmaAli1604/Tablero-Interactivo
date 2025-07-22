import streamlit as st
import pandas as pd
import plotly.express as px

def crear_tabla(df, key_suffix=""):
    """
    Función para crear gráficos interactivos en Streamlit.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos a visualizar.
        key_suffix (str): Sufijo único para las claves de los widgets.
    """
    if not isinstance(df, pd.DataFrame) or df.empty:
        st.error("❌ Error: El dato proporcionado no es un DataFrame válido o está vacío.")
        return

    # Selección del tipo de gráfico
    tipos_graficos = [
        'Gráfico de Dispersión', 'Gráfico de Líneas', 
        'Gráfico de Barras', 'Gráfico de Pastel',
        'Histograma', 'Boxplot', 'Diagrama de Violín',
        'Embudo', 'Mapa de Árbol', 'Rayos de Sol', 'Barras en coordenadas polares'
    ]
    
    tipo_grafico = st.selectbox(
        'Seleccione el tipo de gráfico:',
        tipos_graficos,
        key=f'tipo_grafico_{key_suffix}'
    )

    # Lógica para cada tipo de gráfico
    if tipo_grafico in ['Gráfico de Pastel', 'Histograma']:
        columna = st.selectbox(
            f'Seleccione la columna para el {tipo_grafico}:',
            df.columns,
            key=f'columna_{key_suffix}'
        )
        if tipo_grafico == 'Gráfico de Pastel':
            fig = px.pie(df, names=columna, title=f"{tipo_grafico} - {columna}")
        else:  # Histograma
            fig = px.histogram(df, x=columna, title=f"{tipo_grafico} - {columna}")
        st.plotly_chart(fig, key=f'one_param_{tipo_grafico}_{key_suffix}')
        
    elif tipo_grafico in ['Mapa de Árbol', 'Rayos de Sol']:
        col_x = st.selectbox(
            'Seleccione el eje X:',
            df.columns,
            key=f'GraficoNumX_{key_suffix}'
        )
        col_y = st.selectbox(
            'Seleccione el eje Y:',
            df.select_dtypes(include=["number"]).columns.tolist(),
            key=f'GraficoNumY_{key_suffix}'
        )
        if tipo_grafico == 'Mapa de Árbol':
            fig = px.treemap(df, path=[col_x], values=col_y, title=f"{tipo_grafico} - {col_x} vs {col_y}")
        else:
            fig = px.sunburst(df, path=[col_x], values=col_y, title=f"{tipo_grafico} - {col_x} vs {col_y}")
        st.plotly_chart(fig, key=f'Num_Graph_{tipo_grafico}_{key_suffix}')
        
    elif tipo_grafico == 'Boxplot':
        col_x = st.multiselect("Selecciona las columnas para el eje x:", df.columns, key=f'boxplot_x_{key_suffix}')
        col_y = st.radio(
            'Seleccione la variable numérica:',
            df.select_dtypes(include=['number']).columns,
            key=f'boxplot_y_{key_suffix}'
        )
        if col_x:  # Verifica que se haya seleccionado al menos una columna
            fig = px.box(df, x=col_x, y=col_y, title=f"Boxplot - {col_x} vs {col_y}")
            st.plotly_chart(fig, key=f'boxplot_{key_suffix}')
        else:
            st.warning("⚠️ Selecciona al menos una columna para el eje X.")

    elif tipo_grafico == 'Diagrama de Violín':
        col_y = st.selectbox(
            'Seleccione la variable numérica:',
            df.select_dtypes(include=['number']).columns,
            key=f'violin_{key_suffix}'
        )
        fig = px.violin(df, y=col_y, box=True, points="all", title=f"Diagrama de Violín - {col_y}")
        st.plotly_chart(fig, key=f'plot_violin_{key_suffix}')

    else:  # Gráficos de Dispersión, Líneas y Barras
        col_x = st.selectbox(
            'Seleccione el eje X:',
            df.columns,
            key=f'x_{key_suffix}'
        )
        col_y = st.selectbox(
            'Seleccione el eje Y:',
            df.columns,
            key=f'y_{key_suffix}'
        )
        
        if tipo_grafico == 'Gráfico de Dispersión':
            fig = px.scatter(df, x=col_x, y=col_y, title=f"{tipo_grafico} - {col_x} vs {col_y}")
        elif tipo_grafico == 'Gráfico de Líneas':
            fig = px.line(df, x=col_x, y=col_y, title=f"{tipo_grafico} - {col_x} vs {col_y}")
        elif tipo_grafico == 'Gráfico de Barras':
            fig = px.bar(df, x=col_x, y=col_y, title=f"{tipo_grafico} - {col_x} vs {col_y}")
        elif tipo_grafico == 'Embudo':
            fig = px.funnel(df, x=col_x, y=col_y, title=f"{tipo_grafico} - {col_x} vs {col_y}")
        
        st.plotly_chart(fig, key=f'plot_{tipo_grafico}_{key_suffix}')
        
    st.success("✅ Gráfico creado exitosamente.")