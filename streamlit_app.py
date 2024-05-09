import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report
import sweetviz as sv
import plotly.express as px

# Configurar Streamlit para usar todo el ancho de la pantalla
st.set_page_config(layout="wide")

# Decorador para cachear la carga del DataFrame y evitar recargas innecesarias
@st.cache_data
def cargar_dataframe(archivo):
    try:
        df = pd.read_csv(archivo)
        return df
    except pd.errors.EmptyDataError:
        st.error('El archivo CSV está vacío o no tiene columnas. Por favor, carga un archivo válido.')
        return None

def main():
    # Crear pestañas
    titulos_pestanas = ['Carga de Datos', 'Estadísticas Básicas', 'Análisis EDA', 'Análisis Avanzado', 'Gráficos', 'Acerca de']
    pestañas = st.tabs(titulos_pestanas)

    # Inicialización de variables en el estado de sesión
    if 'df_cargado' not in st.session_state:
        st.session_state.df_cargado = None

    # Agregar contenido a la pestaña de Carga de Datos
    with pestañas[0]:
        st.header('Carga de Datos')
        archivo_cargado = st.file_uploader("Elige un archivo CSV", type=['csv'])
        if archivo_cargado is not None:
            df = cargar_dataframe(archivo_cargado)
            if df is not None:
                st.session_state.df_cargado = df
                st.write(df)

    df = st.session_state.df_cargado

    if df is not None:
        # Pestaña de Estadísticas Básicas
        with pestañas[1]:
            st.header('Estadísticas Básicas')
            st.write('Descripción del DataFrame:')
            st.write(df.describe())
            st.write(df.describe(include='object'))

        # Pestaña de Análisis EDA
        with pestañas[2]:
            st.header('Análisis Exploratorio de Datos (EDA)')
            st.write('Aquí puedes agregar el contenido de análisis EDA')

        # Pestaña de Análisis Avanzado
        with pestañas[3]:
            st.header('Análisis Avanzado')
            profile = ProfileReport(df, explorative=True)
            st_profile_report(profile)

        # Pestaña de Gráficos
        with pestañas[4]:
            st.header('Gráficos')
            columnas_seleccionadas = st.multiselect(
                'Selecciona hasta 6 columnas para graficar:',
                df.columns,
                default=df.columns[:min(6, len(df.columns))].tolist()
            )
            col1, col2 = st.columns(2)
            for i, columna in enumerate(columnas_seleccionadas[:6]):
                with col1 if i % 2 == 0 else col2:
                    if df[columna].dtype == 'object':
                        st.subheader(f'Gráfico de Barras para {columna}')
                        fig = px.bar(df, x=columna, title=f'Gráfico de Barras para {columna}')
                        st.plotly_chart(fig)
                    else:
                        st.subheader(f'Gráfico de Distribución para {columna}')
                        fig = px.histogram(df, x=columna, marginal='rug', title=f'Gráfico de Distribución para {columna}')
                        st.plotly_chart(fig)

    # Pestaña Acerca de
    with pestañas[5]:
        st.header('Acerca de')
        st.write('Esta es una aplicación que te permite navegar entre pestañas y ver análisis de los datos.')

if __name__ == "__main__":
    main()
