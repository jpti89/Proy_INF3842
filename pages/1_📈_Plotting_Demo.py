import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Conceptos que componen el IPC", page_icon="📊")
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

Ponderacion = pd.read_csv('Data/Ponderacion.csv', delimiter=';')

base = alt.Chart(Ponderacion).encode(
    theta=alt.Theta("Ponderacion:Q", stack=True), color=alt.Color("Descripción:N")
).transform_calculate(
    emoji= "{'Alimentos': '🍞', 'Alcohol y tabaco': '🍷', 'Vestuario': '👚', 'Vivienda y servicios': '🏡',  'Equipamiento vivienda': '🛠', 'Salud': '🏥',  'Transporte': '🚌', 'Comunicaciones': '📱', 'Cultura': '🎭', 'Educación': '📚', 'Restaurantes y hoteles': '🏨', 'Bienes y servicios diversos': '📦'}[datum.Descripción]"
)

pie = base.mark_arc(outerRadius=120)
text = base.mark_text(radius=140, size=20).encode(text="Porcentaje:N")
text2 = base.mark_text(radius=170, size=20).encode(text="emoji:N")

st.altair_chart(pie + text + text2, use_container_width=False)
