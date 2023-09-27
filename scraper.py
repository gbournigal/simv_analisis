# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 20:34:38 2023

@author: georg
"""

import requests
import pandas as pd
import re
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

ANOS = [2022, 2023]
MESES = range(1,13)

URL = 'https://seri.simv.gob.do/consulta/fm_limites_niif_2022.php'

def get_soup_url(url):
    response = requests.get(url, verify=False)
    return BeautifulSoup(response.text, 'html.parser')


def get_reportes():
    soup = get_soup_url(URL)
    select_element = soup.find('select', {'name': 'tipo_reporte'})
    if select_element:
        option_elements = select_element.find_all('option')
        return [option.get_text() for option in option_elements]
    

def get_entidades():
    soup = get_soup_url(URL)
    select_element = soup.find('select', {'name': 'entidad_consulta'})
    if select_element:
        option_elements = select_element.find_all('option')
        return [option.get_text() for option in option_elements]

def is_numeric(s):
    return re.match(r'^[-+]?[0-9]*\.?[0-9]+$', s.replace(',', '')) is not None


ENTIDADES = get_entidades()
REPORTES = get_reportes()[:-1]

def get_df_from_web(driver, ano, mes, entidad, reporte):   
    select_element = driver.find_element(By.NAME, 'entidad_consulta')
    select_element.send_keys(entidad)
    
    select_element = driver.find_element(By.NAME, 'tipo_reporte')
    select_element.send_keys(reporte)
    
    fecha_input = driver.find_element(By.NAME, 'filtro_fecha')
    fecha_input.clear()
    fecha_input.send_keys(f'{ano*100+mes}')
    
    consultar_button = driver.find_element(By.NAME, 'consultar')
    consultar_button.click()
    
    current_url = driver.current_url
    
    tables = pd.read_html(current_url, encoding="utf-8")
    df = tables[4]
    df = df.iloc[2:, [0, 1]]
    df.columns = ["cuenta", "valor"]
    df['ano'] = ano
    df['mes'] = mes
    df = df[df['valor'].apply(is_numeric)]
    df['valor'] = df['valor'].str.replace(',', '').astype(float)
    df['entidad'] = entidad
    return df

driver = webdriver.Chrome()
driver.get('https://seri.simv.gob.do/consulta/fm_limites_niif_2022.php')
dfs = []
combinations = list(itertools.product(ANOS, MESES, ENTIDADES, REPORTES))
for ano, mes, entidad, reporte in combinations:
    df = get_df_from_web(driver, ano, mes, entidad, reporte)
    dfs.append(df)
    volver_button = driver.find_element(By.NAME, 'volver')
    volver_button.click()
driver.quit()

result_df = pd.concat(dfs, ignore_index=True)
result_df.to_csv('datos_simv.csv')
