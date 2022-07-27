import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Conceptos IPC", page_icon="📊")
st.markdown("# Conceptos que componen el IPC")

Ponderacion = pd.read_csv('Data/Ponderacion.csv', delimiter=';')

col1, col2 = st.columns(2)

with col1:
    base = alt.Chart(Ponderacion).encode(
    theta=alt.Theta("Ponderacion:Q", stack=True), color=alt.Color("Descripción:N")
    ).transform_calculate(
        emoji= "{'Alimentos': '🍞', 'Alcohol y tabaco': '🍷', 'Vestuario': '👚', 'Vivienda y servicios': '🏡',  'Equipamiento vivienda': '🛠', 'Salud': '🏥',  'Transporte': '🚌', 'Comunicaciones': '📱', 'Cultura': '🎭', 'Educación': '📚', 'Restaurantes y hoteles': '🏨', 'Bienes y servicios diversos': '📦'}[datum.Descripción]"
    )

    pie = base.mark_arc(outerRadius=150).properties(
        width=800,height=500
    )
    text = base.mark_text(radius=170, size=20).encode(text="Porcentaje:N")
    text2 = base.mark_text(radius=210, size=40).encode(text="emoji:N")


    st.altair_chart(pie + text + text2, use_container_width=False)

with col2:
    st.markdown("## ¿Cómo se obtiene el IPC?")
    st.write(
    """Todos los meses encuestadores del INE se encargan de registrar el precio de los productos que consumen los hogares, visitando almacenes de barrio, ferias, supermercados, grandes tiendas, etc. Además, se visitan hogares particulares para consultar valores pagados por arriendo o servicio doméstico.

    Los productos medidos componen la canasta de bienes y servicios, que está compuesta por 321 productos, desde elementos básicos como pan y arroz, hasta productos o servicios de recreación, como una entrada al cine o un televisor. Es de notar que estos 303 productos son los más consumidos por las familias chilenas."""
    )


st.markdown("## Evolución de IPC por concepto")

st.write(
    """Evolución"""
)

Apertura = pd.read_csv('Data/Apertura IPC.csv', delimiter=';')

selection = alt.selection_multi(fields=['Concepto'], bind='legend')

c = alt.Chart(Apertura).mark_area().encode(
    alt.X('Fecha:T', axis=alt.Axis(domain=False, format='%Y', tickSize=0)),
    alt.Y('sum(Valor Ponderado):Q', stack='zero', title='Indice Ponderado'),
    alt.Color('Concepto:N', scale=alt.Scale(scheme='category20b')),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection
).properties(
    width=900
)

st.altair_chart(c, use_container_width=True)