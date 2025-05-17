import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
import sweetviz as sv

# Configuración de la página
st.set_page_config(page_title="EDA Automático", layout="wide")

# Logo de Datos Dinámicos con enlace a la web
st.image("logo.png", width=300)
st.markdown(
    "<a href='https://datosdinamicos.com' target='_blank'>Visita datosdinamicos.com</a>",
    unsafe_allow_html=True
)

st.title("EDA Automático con DATOS DINAMICOS")
st.markdown("Sube un archivo CSV o Excel y elige el método de EDA para generar un reporte HTML interactivo.")

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
        st.stop()

    st.subheader("Vista previa del dataset")
    st.dataframe(df.head())

    # Selección de método de EDA
    eda_tool = st.selectbox(
        "Selecciona método de EDA",
        ["YData Profiling", "Sweetviz"]
    )

    # Si elige Sweetviz, preguntar por variable objetivo
    target = None
    if eda_tool == "Sweetviz":
        if st.checkbox("¿Seleccionar variable objetivo?", value=False):
            target = st.selectbox("Variable objetivo", df.columns.tolist())

    # Botón para generar reporte
    if st.button("Generar reporte EDA"):
        with st.spinner("Generando reporte, espera un momento..."):
            html_report = ""
            if eda_tool == "YData Profiling":
                interactions = {"targets": [target]} if target else None
                profile = ProfileReport(
                    df,
                    title="Reporte EDA",
                    explorative=True,
                    interactions=interactions
                )
                html_report = profile.to_html()
            else:
                # Sweetviz
                if target:
                    report = sv.analyze(df, target_feat=target)
                else:
                    report = sv.analyze(df)
                report.show_html(filepath="sweetviz_report.html", open_browser=False)
                with open("sweetviz_report.html", "r", encoding="utf-8") as f:
                    html_report = f.read()

        st.success("¡Reporte generado con éxito!")

        # Botón para descargar el reporte HTML
        st.download_button(
            label="Descargar reporte HTML",
            data=html_report,
            file_name="eda_report.html",
            mime="text/html"
        )

        # Mostrar reporte embebido
        components.html(html_report, height=700, scrolling=True)
