import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report
import sweetviz as sv


# Configurar Streamlit para usar todo el ancho de la pantalla
st.set_page_config(layout="wide")

# Cargar el DataFrame
def cargar_dataframe(archivo):
    try:
        df = pd.read_csv(archivo)
        return df
    except pd.errors.EmptyDataError:
        st.error('El archivo CSV está vacío o no tiene columnas. Por favor, carga un archivo válido.')
        return None

# Crear pestañas
titulos_pestanas = ['Carga de Datos', 'Estadísticas Básicas', 'Análisis EDA', 'Análisis Avanzado', 'Gráficos', 'Acerca de']
pestaña_carga, pestaña_basicas, pestaña_eda, pestaña_avanzado, pestaña_graficos, pestaña_about = st.tabs(titulos_pestanas)

# Agregar contenido a cada pestaña
with pestaña_carga:
    st.header('Carga de Datos')
    archivo_cargado = st.file_uploader("Elige un archivo CSV", type=['csv'])
    if archivo_cargado is not None:
        df = cargar_dataframe(archivo_cargado)
        if df is not None:
            st.write(df)

with pestaña_basicas:
    st.header('Estadísticas Básicas')
    if archivo_cargado is not None and df is not None:
        st.write('Descripción del DataFrame:')
        st.write(df.describe())
        st.write(df.describe(include='object'))

with pestaña_eda:
    st.header('Análisis Exploratorio de Datos (EDA)')
    st.write('Aquí puedes agregar el contenido de análisis EDA')
    if archivo_cargado is not None:

            if st.button("Generate Sweetviz Report"):
                report = sv.analyze(df)
                # Directamente especificamos la ruta del archivo donde se guardará el reporte
                report_file = 'SWEETVIZ_REPORT1.html'
                # Guardamos el reporte en la ruta especificada
                report.show_html(filepath=report_file, open_browser=False)
                # Usamos un bloque with para asegurarnos de que el archivo se cierre correctamente después de abrirlo
                with open(report_file, 'r', encoding='utf-8') as HtmlFile:
                    source_code = HtmlFile.read()
                    components.html(source_code, height=800, width=1080, scrolling=True)        # Aquí puedes agregar el contenido de análisis EDA
                 
with pestaña_avanzado:
    st.header('Análisis Avanzado')
    if archivo_cargado is not None and df is not None:
        profile = ProfileReport(df, explorative=True)
        st_profile_report(profile)

with pestaña_graficos:
    st.header('Gráficos')
    if archivo_cargado is not None and df is not None:
        # Permitir al usuario seleccionar hasta 6 columnas para graficar
        columnas_seleccionadas = st.multiselect(
            'Selecciona hasta 6 columnas para graficar:',
            df.columns,
            default=df.columns[:min(6, len(df.columns))].tolist()  # Convertir a lista
        )
        # Crear contenedores para 2 columnas
        col1, col2 = st.columns(2)
        for i, columna in enumerate(columnas_seleccionadas[:6]):  # Limitar a 6 gráficos
            with col1 if i % 2 == 0 else col2:  # Alternar entre las dos columnas
                if df[columna].dtype == 'object':  # Datos categóricos
                    st.subheader(f'Gráfico de Barras para {columna}')
                    fig, ax = plt.subplots()
                    df[columna].value_counts().plot(kind='bar', ax=ax)
                    st.pyplot(fig)
                else:  # Datos numéricos
                    st.subheader(f'Gráfico de Distribución para {columna}')
                    fig, ax = plt.subplots()
                    sns.histplot(df[columna], kde=True, ax=ax)
                    st.pyplot(fig)

with pestaña_about:
    st.header('Acerca de')
    st.write('Esta es una aplicación te permite navegar entre pestañas y ver análisis de los datos.')
