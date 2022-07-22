import altair as alt
import pandas as pd
import streamlit as st

st.title("Evolución del Índice de precios al consumidor en Chile ")
df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')

st.set_page_config(
    page_title="IPC Chile", layout="centered"
)

@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["Periodo"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolución de Indices IPC")
        .mark_line()
        .encode(
            x="Periodo",
            y="Indice",
            color="Tipo",
            # strokeDash="symbol",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Periodo)",
            y="Indice",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Periodo", title="Periodo"),
                alt.Tooltip("Indice", title="Indice"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()
    
    

# Original time series chart. Omitted `get_chart` for clarity
chart = get_chart(df)

# Input annotations
ANNOTATIONS = [
    ("Mar 01, 2019", "Inicio Pandemia en Chile"),
]

# Create a chart with annotations
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["Periodo", "Tipo"])
annotations_df.Periodo = pd.to_datetime(annotations_df.Periodo)
annotations_df["Indice"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=15, text="O", dx=-14, dy=10, align="center")
    .encode(
        x="Periodo:T",
        y=alt.Y("Indice:Q"),
        tooltip=["Tipo"],
    )
    .interactive()
)

# Display both charts together
st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)