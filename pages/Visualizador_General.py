# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:34:28 2023

@author: gbournigal
"""

import streamlit as st
import pandas as pd
import plotly.graph_objs as go


st.set_page_config(
     layout="wide",
 )

st.title("""Visualizador General""")

entidad_mapping = {
    "ALPHA SOCIEDAD DE VALORES, S.A.": "Alpha",
    "BHD PUESTO DE BOLSA, S.A. ": "BHD",
    "CCI PUESTO DE BOLSA, S.A.": "CCI",
    "EXCEL PUESTO DE BOLSA, S.A.": "Excel",
    "INVERSIONES & RESERVAS, S.A.- PUESTO DE BOLSA": "Reservas",
    "INVERSIONES POPULAR, S.A. PUESTO DE BOLSA": "Popular",
    "INVERSIONES SANTA CRUZ PUESTO DE BOLSA, S.A.": "Santa Cruz",
    "JMMB PUESTO DE BOLSA, S.A.": "JMMB",
    "MPB MULTIVALORES, S.A.": "MPB Multivalores",
    "PARALLAX VALORES PUESTO DE BOLSA, S.A. (PARVAL) ": "Parval",
    "PRIMMA VALORES, S.A. PUESTO DE BOLSA": "Primma",
    "TIVALSA, S.A.": "Primma",
    "UC- UNITED CAPITAL PUESTO DE BOLSA, S.A.": "United",
    "VERTEX VALORES PUESTO DE BOLSA, S.A.": "Vertex",
}


df = pd.read_csv("datos/datos_simv.csv")
df = df[
    df["entidad"]
    != "CITINVERSIONES DE TITULOS Y VALORES, S.A. PUESTO DE BOLSA"
]
df["entidad"] = df["entidad"].replace(entidad_mapping)


entidad = st.selectbox("Seleccionar entidad", sorted(df.entidad.unique()), 7)
variable = st.selectbox(
    "Seleccionar Variable",
    df.cuenta.unique(),
    0,
)

def general_plot(df, entidad, variable):
    df = df[df['entidad'] == entidad]
    df = df[df['cuenta'] == variable]
    df["fecha"] = pd.to_datetime(
        df["ano"].astype(str) + df["mes"].astype(str).str.zfill(2),
        format="%Y%m",
    )
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["fecha"],
            y=df["valor"],
            name=f"{variable}",
        ),
    )
    fig.update_layout(
        title_text=f"<b>Serie de tiempo {variable}</b><br>{entidad}",
        xaxis_title=variable,
        template="plotly_white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        title_x=0.3,
        title_y=0.95,
    )
    return fig

st.plotly_chart(general_plot(df, entidad, variable), 
                use_container_width=True)
