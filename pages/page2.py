import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

df = pd.read_csv('Data/Apertura IPC.csv', delimiter=';')

selection = alt.selection_multi(fields=['Concepto'], bind='legend')

st.alt.Chart(Apertura).mark_area().encode(
    alt.X('Fecha:T', axis=alt.Axis(domain=False, format='%Y', tickSize=0)),
    alt.Y('sum(Valor Ponderado):Q', stack='zero', title='Indice Ponderado'),
    alt.Color('Concepto:N', scale=alt.Scale(scheme='category20b')),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection
).properties(
    width=900
)