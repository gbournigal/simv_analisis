# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:06:31 2023

@author: gbournigal
"""

import streamlit as st


st.set_page_config(
     page_title="""Análisis Datos SIMV""",
     # page_icon="⚾",
     layout="wide",
 )

st.title("""Análisis financiero SIMV""")

st.write("""
         Toda la data utilizada viene de la [SIMV](https://seri.simv.gob.do/consulta/fm_limites_niif_2022.php).
         Se utilizó [Sellenium](https://www.selenium.dev/) y [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) para extraer los datos y guardarlos en csv.
         El repositorio con el código está público en [Github](https://github.com/gbournigal/simv_analisis).
         El csv se puede descargar desde el repositorio. En los dos tabs a la izquierda se puede visualizar la data.
         """)
         
         