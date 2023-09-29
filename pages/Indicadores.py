# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:14:25 2023

@author: gbournigal
"""

import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(
     layout="wide",
 )

st.title("""Indicadores Creados""")

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


df = pd.read_csv("datos_simv.csv")
df = df[
    df["entidad"]
    != "CITINVERSIONES DE TITULOS Y VALORES, S.A. PUESTO DE BOLSA"
]
df["entidad"] = df["entidad"].replace(entidad_mapping)


def get_solvencia():
    total_activos = df[df["cuenta"].str.contains("TOTAL DE ACTIVOS")]
    total_activos_sum = total_activos.groupby(["entidad", "ano", "mes"])[
        "valor"
    ].sum()
    total_activos_sistema = total_activos.groupby(["ano", "mes"])[
        "valor"
    ].sum()

    total_patrimonio = df[df["cuenta"].str.contains("TOTAL DE PATRIMONIO")]
    total_patrimonio_sum = total_patrimonio.groupby(["entidad", "ano", "mes"])[
        "valor"
    ].sum()
    total_patrimonio_sistema = total_patrimonio.groupby(["ano", "mes"])[
        "valor"
    ].sum()

    ratio_solvencia = total_patrimonio_sum / total_activos_sum
    ratio_solvencia = ratio_solvencia.reset_index()

    ratio_solvencia_sistema = total_patrimonio_sistema / total_activos_sistema
    ratio_solvencia_sistema = ratio_solvencia_sistema.reset_index()
    ratio_solvencia_sistema["entidad"] = "TOTAL"
    return pd.concat([ratio_solvencia, ratio_solvencia_sistema])


def get_rentabilidad():
    resultados_financieros = df[
        df["cuenta"].str.contains(
            "Total resultados por instrumentos financieros"
        )
    ]
    resultados_financieros_sum = resultados_financieros.groupby(
        ["entidad", "ano", "mes"]
    )["valor"].sum()
    resultados_financieros_sistema = resultados_financieros.groupby(
        ["ano", "mes"]
    )["valor"].sum()

    utilidad_ejerc = df[df["cuenta"].str.contains("UTILIDAD DEL EJERCICIO")]
    utilidad_ejerc_sum = utilidad_ejerc.groupby(["entidad", "ano", "mes"])[
        "valor"
    ].sum()
    utilidad_ejerc_sistema = utilidad_ejerc.groupby(["ano", "mes"])[
        "valor"
    ].sum()

    rentabilidad = (utilidad_ejerc_sum) / resultados_financieros_sum
    rentabilidad = rentabilidad.reset_index()

    rentabilidad_sistema = (
        utilidad_ejerc_sistema / resultados_financieros_sistema
    )
    rentabilidad_sistema = rentabilidad_sistema.reset_index()
    rentabilidad_sistema["entidad"] = "TOTAL"
    return pd.concat([rentabilidad, rentabilidad_sistema])


def get_liquidez():
    efectivo = df[
        df["cuenta"].str.contains("Efectivo y equivalente de efectivo")
    ]
    efectivo_sum = efectivo.groupby(["entidad", "ano", "mes"])["valor"].sum()
    efectivo_sistema = efectivo.groupby(["ano", "mes"])["valor"].sum()

    pasivos_finan = df[df["cuenta"].str.contains("TOTAL DE PASIVOS")]
    pasivos_finan_sum = pasivos_finan.groupby(["entidad", "ano", "mes"])[
        "valor"
    ].sum()
    pasivos_finan_sistema = pasivos_finan.groupby(["ano", "mes"])[
        "valor"
    ].sum()

    liquidez = (efectivo_sum) / pasivos_finan_sum
    liquidez = liquidez.reset_index()

    liquidez_sistema = efectivo_sistema / pasivos_finan_sistema
    liquidez_sistema = liquidez_sistema.reset_index()
    liquidez_sistema["entidad"] = "TOTAL"
    return pd.concat([liquidez, liquidez_sistema])


def plot_barras_st(dfs, indicador, ano, mes):
    df = dfs[indicador]
    df["valor"] = df["valor"] * 100
    df = df[(df["ano"] == ano) & (df["mes"] == mes)]
    df = df.sort_values("valor")
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["entidad"],
            y=df["valor"],
            marker=dict(
                color=df["valor"],
                colorscale="RdBu",
            ),
            name=indicador,
        ),
    )

    fig.update_layout(
        title_text=f"<b>Comparativo {indicador}</b><br> {mes}-{ano}",
        xaxis_title=indicador,
        yaxis_title="%",
        template="plotly_white",
        title_x=0.3,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )
    return fig


def plot_serie_entidad_v_sistema(dfs, indicador, entidad):
    df = dfs[indicador]
    df["valor"] = df["valor"] * 100
    df["fecha"] = pd.to_datetime(
        df["ano"].astype(str) + df["mes"].astype(str).str.zfill(2),
        format="%Y%m",
    )
    df_sistema = df[df["entidad"] == "TOTAL"]
    df_popular = df[df["entidad"] == entidad]
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_sistema["fecha"],
            y=df_sistema["valor"],
            name=f"{indicador} Sistema",
            line=dict(dash="dash"),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=df_popular["fecha"],
            y=df_popular["valor"],
            name=f"{indicador} {entidad}",
        ),
    )

    fig.update_layout(
        title_text=f"<b>Serie de tiempo {indicador}</b>",
        xaxis_title=indicador,
        yaxis_title="%",
        template="plotly_white",
        title_x=0.3,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=0.95,
            yanchor="bottom",
        ),
        margin=dict(t=100),
    )
    return fig


solvencia = get_solvencia()
rentabilidad = get_rentabilidad()
liquidez = get_liquidez()

dfs = {
    "Solvencia": solvencia,
    "Rentabilidad Financiera / Utilidades": rentabilidad,
    "Efectivo / Pasivos": liquidez,
}


indicador = st.selectbox(
    "Seleccionar Indicador",
    [
        "Solvencia",
        "Rentabilidad Financiera / Utilidades",
        "Efectivo / Pasivos",
    ],
    0,
)

col1, col2 = st.columns(2)

with col1:
    ano = st.selectbox("Seleccionar año", df.ano.unique(), 1)
    mes = st.selectbox("Seleccionar mes", df.mes.unique(), 7)
    st.plotly_chart(plot_barras_st(dfs, indicador, ano, mes), 
                    use_container_width=True)
    

with col2:
    entidad = st.selectbox("Seleccionar entidad", sorted(df.entidad.unique()), 7)
    st.plotly_chart(plot_serie_entidad_v_sistema(dfs, indicador, entidad), 
                    use_container_width=True)
