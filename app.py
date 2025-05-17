import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="EDA Automático", layout="wide")

# Logo de Datos Dinámicos, clic para ir a la web

st.image("logo.png", width=300)
st.markdown(
    "<a href='https://datosdinamicos.com' target='_blank'>Datos Dinamicos </a>",
    unsafe_allow_html=True
)

st.title("EDA Automático con DATOS DINAMICOS")
st.markdown("Sube un archivo CSV o Excel y genera un reporte HTML interactivo de EDA.")

# Carga de archivo CSV o Excel
uploaded_file = st.file_uploader(
    "Selecciona tu archivo CSV o Excel",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file:
    try:
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext in ["xls", "xlsx"]:
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
    else:
        st.subheader("Vista previa del dataset")
        st.dataframe(df.head())

        if st.button("Generar reporte EDA"):
            with st.spinner("Generando reporte, espera un momento..."):
                profile = ProfileReport(
                    df,
                    title="Reporte EDA",
                    explorative=True
                )
                html_report = profile.to_html()

            st.success("¡Reporte generado con éxito!")

            # Descargar reporte HTML
            st.download_button(
                label="Descargar reporte HTML",
                data=html_report,
                file_name="eda_report.html",
                mime="text/html"
            )

            # Mostrar reporte embebido
            components.html(html_report, height=700, scrolling=True)

