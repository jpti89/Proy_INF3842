import altair as alt
import pandas as pd
import streamlit as st

st.title("Hola Mundo!!!")
df = pd.read_csv('Data/indice_IPC.csv', delimiter=';')

#st.set_page_config(
#    page_title="Time series annotations", page_icon="⬇", layout="centered"
#)
st.write(df.head(5))