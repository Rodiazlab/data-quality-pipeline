import streamlit as st
import json
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="Calidad de datos",
    layout="wide"
)

st.title("Calidad de datos")
st.write("Panel de métricas del pipeline")

metrics_dir = Path(__file__).resolve().parent / "data" / "metrics"
metrics_files = sorted(metrics_dir.glob("quality_summary_*.json"))

if not metrics_files:
    st.warning("No hay archivos de métricas disponibles.")
    st.stop()

metrics_path = st.selectbox(
    "Selecciona una ejecución",
    options=metrics_files,
    format_func=lambda path: path.name
)
st.caption(f"Archivo seleccionado: {metrics_path.name}")

with metrics_path.open(encoding="utf-8") as file:
    summary = json.load(file)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Registros recibidos", summary["received_records"])

with col2:
    st.metric("Registros válidos", summary["valid_records"])

with col3:
    st.metric("Registros en cuarentena", summary["quarantine_records"])

st.subheader("Porcentajes de calidad")

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Registros válidos",
        f"{summary['valid_percentage']:.1f}%"
    )

with col5:
    st.metric(
        "Registros en cuarentena",
        f"{summary['quarantine_percentage']:.1f}%"
    )

st.subheader("Incidencias por motivo")

if summary["quality_issues"]:
    issues_df = pd.DataFrame(
        summary["quality_issues"].items(),
        columns=["Motivo", "Incidencias"]
    )

    st.bar_chart(
        issues_df,
        x="Motivo",
        y="Incidencias",
        horizontal=True
    )

    st.caption("Un registro puede tener más de una incidencia.")
else:
    st.success("No se detectaron incidencias.")