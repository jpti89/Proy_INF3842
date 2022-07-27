import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Conceptos IPC", page_icon="📊")
st.markdown("# Conceptos que componen el IPC")

st.write(
    """Conceptos"""
)

Ponderacion = pd.read_csv('Data/Ponderacion.csv', delimiter=';')

base = alt.Chart(Ponderacion).encode(
    theta=alt.Theta("Ponderacion:Q", stack=True), color=alt.Color("Descripción:N")
).transform_calculate(
    emoji= "{'Alimentos': '🍞', 'Alcohol y tabaco': '🍷', 'Vestuario': '👚', 'Vivienda y servicios': '🏡',  'Equipamiento vivienda': '🛠', 'Salud': '🏥',  'Transporte': '🚌', 'Comunicaciones': '📱', 'Cultura': '🎭', 'Educación': '📚', 'Restaurantes y hoteles': '🏨', 'Bienes y servicios diversos': '📦'}[datum.Descripción]"
)

pie = base.mark_arc(outerRadius=150).properties(
    width=600,height=500
)
text = base.mark_text(radius=170, size=20).encode(text="Porcentaje:N")
text2 = base.mark_text(radius=210, size=40).encode(text="emoji:N")


st.altair_chart(pie + text + text2, use_container_width=False)
