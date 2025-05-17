# app.py
# Requisitos: 
#   pip install streamlit ydata-profiling pandas

import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="EDA Automático", layout="wide")

st.title("EDA Automático con YData Profiling")
st.markdown("Sube un archivo CSV y genera un reporte HTML interactivo de EDA.")

# Carga de archivo CSV
uploaded_file = st.file_uploader("Selecciona tu archivo CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
    else:
        st.subheader("Vista previa del dataset")
        st.dataframe(df.head())

        if st.button("Generar reporte EDA"):
            with st.spinner("Generando reporte, espera un momento..."):
                # Genera el ProfileReport
                profile = ProfileReport(
                    df,
                    title="Reporte EDA",
                    explorative=True
                )
                # Convierte a HTML
                html_report = profile.to_html()

            st.success("¡Reporte generado con éxito!")

            # Botón para descargar el reporte HTML
            st.download_button(
                label="Descargar reporte HTML",
                data=html_report,
                file_name="eda_report.html",
                mime="text/html"
            )

            # Muestra el reporte embebido
            components.html(html_report, height=700, scrolling=True)
