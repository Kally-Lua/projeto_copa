import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.DataFrame({
"Mês": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
"Vendas": [120, 145, 98, 200, 175, 230],
"Clientes": [40, 55, 35, 80, 70, 95],
})

st.title("Dashboard teste")
st.header ("Luana")
st.write ("Esse é um texto simples")

st.dataframe(df, use_container_width =True)