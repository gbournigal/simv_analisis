# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd


df = pd.read_csv('datos_simv.csv')
df = df[df['entidad'] != 'CITINVERSIONES DE TITULOS Y VALORES, S.A. PUESTO DE BOLSA']

def get_solvencia():
    total_activos = df[df['cuenta'].str.contains('TOTAL DE ACTIVOS')]
    total_activos_sum = total_activos.groupby(['entidad', 'ano', 'mes'])['valor'].sum()
    total_activos_sistema = total_activos.groupby(['ano', 'mes'])['valor'].sum()
    
    total_patrimonio = df[df['cuenta'].str.contains('TOTAL DE PATRIMONIO')]
    total_patrimonio_sum = total_patrimonio.groupby(['entidad', 'ano', 'mes'])['valor'].sum()
    total_patrimonio_sistema = total_patrimonio.groupby(['ano', 'mes'])['valor'].sum()
    
    ratio_solvencia = total_patrimonio_sum / total_activos_sum
    ratio_solvencia = ratio_solvencia.reset_index()
    
    ratio_solvencia_sistema = total_patrimonio_sistema / total_activos_sistema
    ratio_solvencia_sistema = ratio_solvencia_sistema.reset_index()
    ratio_solvencia_sistema['entidad'] = 'TOTAL'
    return pd.concat([ratio_solvencia, ratio_solvencia_sistema])


def get_rentabilidad():
    resultados_financieros = df[df['cuenta'].str.contains('Total resultados por instrumentos financieros')]
    resultados_financieros_sum = resultados_financieros.groupby(['entidad', 'ano', 'mes'])['valor'].sum()
    resultados_financieros_sistema = resultados_financieros.groupby(['ano', 'mes'])['valor'].sum()
    
    utilidad_ejerc = df[df['cuenta'].str.contains('UTILIDAD DEL EJERCICIO')]
    utilidad_ejerc_sum = utilidad_ejerc.groupby(['entidad', 'ano', 'mes'])['valor'].sum()
    utilidad_ejerc_sistema = utilidad_ejerc.groupby(['ano', 'mes'])['valor'].sum()
    
    rentabilidad = (utilidad_ejerc_sum) / resultados_financieros_sum
    rentabilidad = rentabilidad.reset_index()
    
    rentabilidad_sistema = utilidad_ejerc_sistema / resultados_financieros_sistema
    rentabilidad_sistema = rentabilidad_sistema.reset_index()
    rentabilidad_sistema['entidad'] = 'TOTAL'
    return pd.concat([rentabilidad, rentabilidad_sistema])

