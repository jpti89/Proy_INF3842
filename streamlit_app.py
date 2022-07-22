import altair as alt
import pandas as pd
import streamlit as st

st.title("Hola Mundo!!!")
df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')

st.set_page_config(
    page_title="Time series annotations", page_icon="⬇", layout="centered"
)

@st.experimental_memo(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolution of stock prices")
        .mark_line()
        .encode(
            x="date",
            y="price",
            color="symbol",
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
            x="yearmonthdate(date)",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("price", title="Price (USD)"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()
    
    

# Original time series chart. Omitted `get_chart` for clarity
chart = get_chart(df)

# Input annotations
ANNOTATIONS = [
    ("Mar 01, 2018", "Pretty good day for GOOG"),
    ("Dec 01, 2017", "Something's going wrong for GOOG & AAPL"),
    ("Nov 01, 2018", "Market starts again thanks to..."),
    ("Dec 01, 2019", "Small crash for GOOG after..."),
]

# Create a chart with annotations
annotations_df = pd.DataFrame(ANNOTATIONS, columns=["Periodo", "Tipo"])
annotations_df.date = pd.to_datetime(annotations_df.date)
annotations_df["Indice"] = 0
annotation_layer = (
    alt.Chart(annotations_df)
    .mark_text(size=15, text="⬇", dx=-14, dy=10, align="center")
    .encode(
        x="Periodo:T",
        y=alt.Y("Indice:Q"),
        tooltip=["Tipo"],
    )
    .interactive()
)

# Display both charts together
st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)