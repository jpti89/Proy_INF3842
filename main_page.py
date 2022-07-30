import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

def main_page():

    st.title("Evolución del IPC en Chile ")
    df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## ¿Qué es el IPC?")
        st.write(
        """El Índice de Precios al Consumidor (IPC) es un indicador económico elaborado y publicado por el INE, que mide mes a mes la variación conjunta de los precios de una canasta de bienes y servicios representativa del consumo de los hogares del país."""
        )
        

    with col2:
        st.image("img/02-ipc.jpg")

    col3, col4 = st.columns(2)
    
    with col3:
        st.image("img/03-ipc.png")
        

    with col4:
        st.markdown("## ¿Para qué se usa el IPC?")
        st.write(
        """Este indicador se usa frecuentemente para reajustar arriendos, créditos, sueldos y salarios, y diferentes contratos públicos y privados. Además, se usa para reajustar diversas tarifas reguladas por la autoridad como los servicios básicos por ejemplo, electricidad y agua potable, locomoción colectiva, entre otros. El IPC también se utiliza para el cálculo de la Unidad de Fomento (UF) y la Unidad Tributaria Mensual (UTM)."""
        )
        
       
    st.markdown("### Prueba haciendo Zoom en el siguiente grafico para ver su evolución en el tiempo")
    
    st.sidebar.success("⬆️ Ir a la otra pagina para saber de lo que se compone el IPC")
    
    @st.experimental_memo(ttl=60 * 60 * 24)
    def get_chart(data):
        hover = alt.selection_single(
            fields=["Periodo"],
            nearest=True,
            on="mouseover",
            empty="none",
        )
        
        lines = alt.Chart(data).mark_line().encode(
        alt.Y('Indice:Q',
            scale=alt.Scale(domain=(90, 130))
        ),
        x='Periodo:T'
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
                    alt.Tooltip("Periodo:T", title="Periodo"),
                    alt.Tooltip("Indice", title="Indice"),
                    alt.Tooltip("Varacion porcentual", title="Varacion Mes"),
                ],
            )
            .add_selection(hover)
        )

        return (lines + points + tooltips).interactive()
        
        
    chart = get_chart(df)

    ANNOTATIONS = [
        ("2019-04-01", "Inicio Pandemia en Chile"),
    ]

    annotations_df = pd.DataFrame(ANNOTATIONS, columns=["Periodo","Tipo"])
    annotations_df.Periodo = pd.to_datetime(annotations_df.Periodo)
    annotations_df["Indice"] = 0
    annotation_layer = (
        alt.Chart(annotations_df)
        .mark_text(size=15, text="O", dx=-14, dy=10, align="center")
        .encode(
            x="Periodo:T",
            y=alt.Y("Indice:Q"),
        )
        .interactive()
    ).properties(
    height=500
    )

    st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)



if __name__ == "__main__":
    main_page()