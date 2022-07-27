import altair as alt
import pandas as pd
import streamlit as st

def main_page():

    st.title("Evolución del IPC en Chile ")
    df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')
    
    st.markdown("## ¿Qué es el IPC?")
    st.write(
    """El Índice de Precios al Consumidor (IPC) es un indicador económico elaborado y publicado por el INE, que mide mes a mes la variación conjunta de los precios de una canasta de bienes y servicios representativa del consumo de los hogares del país."""
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
            )
        )


        points = lines.transform_filter(hover).mark_circle(size=65)


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
        
        
    chart = get_chart(df)

    ANNOTATIONS = [
        ("2019-04-01", "Inicio Pandemia en Chile"),
    ]

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
    ).properties(
    height=500
    )

    st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)



if __name__ == "__main__":
    main_page()