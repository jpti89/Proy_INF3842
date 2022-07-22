import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title("Hola Mundo!!!")
df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')

highlight = alt.selection(type='single', on='mouseover',
                          fields=['symbol'], nearest=True)

base = alt.Chart(df).encode(
    x='Periodo:T',
    y='Indice:Q',
    color='Tipo:N'
)

points = base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
).properties(
    width=600
)

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

points + lines