import altair as alt
import pandas as pd
import streamlit as st

st.title("Hola Mundo!!!")
df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')

# Original time series chart. Omitted `get_chart` for clarity
chart = get_chart(df)

# Input annotations
ANNOTATIONS = [
#    ("Mar 01, 2008", "Pretty good day for GOOG"),
#    ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
#    ("Nov 01, 2008", "Market starts again thanks to..."),
#    ("Dec 01, 2009", "Small crash for GOOG after..."),
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