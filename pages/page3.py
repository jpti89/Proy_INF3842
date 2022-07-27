import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)
Apertura = pd.read_csv('Data/Apertura IPC.csv', delimiter=';')

highlight = alt.selection(type='single', on='mouseover',
                          fields=['Concepto'], nearest=True)

base = alt.Chart(Apertura).encode(
    x='Fecha:T',
    y='Variación porcentual:Q',
    color='Concepto:N'
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

st.altair_chart(lines + points, use_container_width=True)