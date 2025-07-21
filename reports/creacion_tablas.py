import streamlit as st
import plotly.express as px
import pandas as pd


def un_valor_grafica(tabla,value,df):
    match tabla:
        case "Pie":
            st.subheader("Gráfico de Pie")
            fig = px.pie(df, names=value, title=f"Gráfico de Pie de {value}")
            st.plotly_chart(fig)
        case "Histograma":
            st.subheader("Gráfico de Histograma")
            if value in df.columns:
                fig = px.histogram(df, x=value,title=f"Gráfico de Histograma de {value}")
                st.plotly_chart(fig)
            else:
                st.error(f"La columna '{value}' no existe en el DataFrame.")

def dos_valor_grafica(tabla,x,y,df):
    match tabla:
        case "Dispersion":
            st.subheader("Gráfico de Dispersión")
            fig = px.scatter(df, x=x, y=y)
            st.plotly_chart(fig)
        case "Línea":
            st.subheader("Gráfico de Línea")
            fig = px.line(df, x=x, y=y)
            st.plotly_chart(fig)
        case "Barras":
            st.subheader("Gráfico de Barras")
            fig = px.bar(df, x=x, y=y)
            st.plotly_chart(fig)
        case "Barras en coordenadas polares":
            st.subheader("Gráfico de Barras en Coordenadas Polares")
            fig = px.bar_polar(df, r=y, theta=x)
            st.plotly_chart(fig)
        case "Embudo":
            st.subheader("Gráfico Embudo")
            fig = px.funnel(df, x=x, y=y)
            st.plotly_chart(fig)
            
def grafica_boxplot(df):
    x_axis = st.multiselect("Selecciona las columnas para el eje x:", df.columns)
    y_axis = st.radio("Selecciona el eje y: ", df.columns)
    fig = px.box(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig)
    
def grafica_dviolin(df):
    x = st.selectbox("Selecciona el eje x: ",df.select_dtypes(include="object").columns)
    y = st.selectbox("Selecciona el eje y: ", df.select_dtypes(include="number").columns)
    box = st.selectbox("Visualizar con caja: ", ["Si","No"])
    categoria = st.selectbox("Selecciona la categoría: ", df.select_dtypes(include=["object", "category"]).columns)
    flag = False
    if box == "Si":
        flag = True
    
    st.subheader("Diagrama de Violín")
    fig = px.violin(df, y=y, x=x, box=flag, color=categoria, hover_data=df.columns)
    st.plotly_chart(fig)
            

def grafica_numerica(df,tabla,x,y):
    match tabla:
        case "Rayos de Sol":
            fig = px.sunburst(df, path=[x], values=y)
            st.plotly_chart(fig)
        case "Mapa de árbol":
            fig = px.treemap(df, path=[x], values=y)
            st.plotly_chart(fig)
        
        
def crear_tabla(df,key_suffix=""):

    graficos=["Dispersion","Línea","Barras","Barras en coordenadas polares","Boxplot","Diagrama de violin","Histograma","Pie","Embudo","Mapa de árbol","Rayos de Sol"]
    columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
    
    dataset_choice = st.selectbox(
        "Selecciona la tabla:",
        graficos,
        key=f"dataset_choice_{hash(str(df))}" if key_suffix else None
    )
    
    if dataset_choice in ("Pie","Histograma")  :
        value = st.selectbox("Selecciona el valor: ",df.columns)
        un_valor_grafica(dataset_choice,value,df)    
    elif dataset_choice == "Boxplot":
        grafica_boxplot(df)
    elif dataset_choice == "Diagrama de violin":
        grafica_dviolin(df)
    elif dataset_choice in ("Mapa de árbol","Rayos de Sol"):
        x_axis = st.selectbox("Selecciona el eje x: ",df.columns)
        value = st.selectbox("Selecciona el valor del eje y: ",columnas_numericas)
        grafica_numerica(df,dataset_choice,x_axis,y_axis)
    else:
        x_axis = st.selectbox("Selecciona el eje x: ",df.columns)
        y_axis = st.selectbox("Selecciona el eje y: ",df.columns)
        dos_valor_grafica(dataset_choice,x_axis,y_axis,df)
            