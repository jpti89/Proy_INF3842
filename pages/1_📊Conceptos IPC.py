import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Conceptos IPC", page_icon="📊", layout="wide")
st.markdown("# Conceptos que componen el IPC")

Ponderacion = pd.read_csv('Data/Ponderacion.csv', delimiter=';')

colors = ['#ffb3ba',
          '#ffdfba',
          '#ffffba',
          '#baffc9',
          '#bae1ff',
          '#96ceb4',
          '#ffeead',
          '#ff6f69',
          '#ffcc5c',
          '#88d8b0',
          '#e1f7d5',
          '#c9c9ff'
          ]
          
col1, col2 = st.columns(2)

with col1:
    base = alt.Chart(Ponderacion).encode(
    theta=alt.Theta("Ponderacion:Q", stack=True), color=alt.Color("Descripción:N", legend= None,scale=alt.Scale(range= colors))
    ).transform_calculate(
        emoji= "{'Alimentos': '🍞', 'Alcohol y tabaco': '🍷', 'Vestuario': '👚', 'Vivienda y servicios': '🏡',  'Equipamiento vivienda': '🛠', 'Salud': '🏥',  'Transporte': '🚌', 'Comunicaciones': '📱', 'Cultura': '🎭', 'Educación': '📚', 'Restaurantes y hoteles': '🏨', 'Bienes y servicios diversos': '📦'}[datum.Descripción]"
    ).properties(
    width=800,height=500
    )

    pie = base.mark_arc(outerRadius=130)
    text = base.mark_text(radius=160, size=20).encode(text="Porcentaje:N")
    text2 = base.mark_text(radius=225, size=30).encode(text="emoji:N")


    st.altair_chart(pie + text + text2, use_container_width=False)

with col2:
    st.markdown("## ¿Cómo se obtiene el IPC?")
    st.write(
    """Todos los meses encuestadores del INE se encargan de registrar el precio de los productos que consumen los hogares, visitando almacenes de barrio, ferias, supermercados, grandes tiendas, etc. Además, se visitan hogares particulares para consultar valores pagados por arriendo o servicio domestico.
    Los productos medidos componen la canasta de bienes y servicios, que está compuesta por 321 productos, desde elementos básicos como pan y arroz, hasta productos o servicios de recreación, como una entrada al cine o un televisor. Es de notar que estos 303 productos son los mÃ¡s consumidos por las familias chilenas."""
    )


st.sidebar.success("⚙ Si el grafico y texto se ve mal, prueba cambiando la configuración a Wide Mode")

st.markdown("## Evolución de IPC por concepto")

st.markdown("### Prueba presionando en cada concepto a la derecha del grafico de abajo")

Apertura = pd.read_csv('Data/Apertura IPC.csv', delimiter=';')

selection = alt.selection_multi(fields=['Concepto'], bind='legend')

c = alt.Chart(Apertura).mark_area().encode(
    alt.X('Fecha:T', axis=alt.Axis(domain=False, format='%Y', tickSize=0)),
    alt.Y('sum(Valor Ponderado):Q', stack='zero', title='Indice Ponderado'),
    alt.Color('Concepto:N', scale=alt.Scale(range= colors)),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection
).properties(
    width=900
)

st.altair_chart(c, use_container_width=True)