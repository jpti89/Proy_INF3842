import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Conceptos IPC", page_icon="馃搳")
st.markdown("# Conceptos que componen el IPC")

Ponderacion = pd.read_csv('Data/Ponderacion.csv', delimiter=';')

col1, col2 = st.columns(2)

with col1:
    base = alt.Chart(Ponderacion).encode(
    theta=alt.Theta("Ponderacion:Q", stack=True), color=alt.Color("Descripci贸n:N")
    ).transform_calculate(
        emoji= "{'Alimentos': '馃崬', 'Alcohol y tabaco': '馃嵎', 'Vestuario': '馃憵', 'Vivienda y servicios': '馃彙',  'Equipamiento vivienda': '馃洜', 'Salud': '馃彞',  'Transporte': '馃殞', 'Comunicaciones': '馃摫', 'Cultura': '馃幁', 'Educaci贸n': '馃摎', 'Restaurantes y hoteles': '馃彣', 'Bienes y servicios diversos': '馃摝'}[datum.Descripci贸n]"
    )

    pie = base.mark_arc(outerRadius=150).properties(
        width=800,height=500
    )
    text = base.mark_text(radius=170, size=20).encode(text="Porcentaje:N")
    text2 = base.mark_text(radius=210, size=40).encode(text="emoji:N")


    st.altair_chart(pie + text + text2, use_container_width=False)

with col2:
    st.markdown("## 驴C贸mo se obtiene el IPC?")
    st.write(
    """Todos los meses encuestadores del INE se encargan de registrar el precio de los productos que consumen los hogares, visitando almacenes de barrio, ferias, supermercados, grandes tiendas, etc. Adem谩s, se visitan hogares particulares para consultar valores pagados por arriendo o servicio dom茅stico.
    Los productos medidos componen la canasta de bienes y servicios, que est谩 compuesta por 321 productos, desde elementos b谩sicos como pan y arroz, hasta productos o servicios de recreaci贸n, como una entrada al cine o un televisor. Es de notar que estos 303 productos son los m谩s consumidos por las familias chilenas."""
    )

st.sidebar.success("Si el grafico y texto se ve mal, prueba cambiando la configuración a Wide Mode")

st.markdown("## Evoluci贸n de IPC por concepto")

st.markdown("### Prueba presionando en cada concepto a la derecha del grafico de abajo")

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