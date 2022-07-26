import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="IPC Chile", layout="centered"
)

def main_page():


    st.title("Evolución del Índice de precios al consumidor en Chile ")
    df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')

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

def page2():
    import streamlit as st
    import altair as alt
    import pandas as pd

    st.set_page_config(page_title="Plotting Demo", page_icon="📈")

    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

    df = pd.read_csv('Data/Apertura.csv', delimiter=';')

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

def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()