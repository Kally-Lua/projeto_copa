import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1 - Jogadores por posição

def grafico_posicoes(df):

    dados = (
        df.groupby("posicao")
        .size()
        .reset_index(name="Quantidade")
        .sort_values("Quantidade", ascending=True)
    )

    fig = px.bar(
        dados,
        x="Quantidade",
        y="posicao",
        orientation="h",
        color="Quantidade",
        title="Jogadores por Posição",
        color_discrete_sequence=["#2e7d32"], 
        text="Quantidade",
        labels={"posicao": "Posição", "Quantidade": "Quantidade de Jogadores"}  
    )
    #adicionei essa funcionalidade para que os números fiquem fora da barra e 
    fig.update_traces(textposition="outside")
    #E essa abaixo é para configurar o layout do gráfico, como altura e títulos dos eixos
    fig.update_layout(
        template="plotly_white",
        yaxis_title="Posição",
        xaxis_title="Quantidade de Jogadores"
    )

    st.plotly_chart(fig, use_container_width=True)

# 2 - Top 10 Artilheiros
def grafico_top_gols(df):

    dados = (
        df.sort_values("gols_clube", ascending=False)
        .head(10)
    )

    fig = px.bar(
        dados,
        x="gols_clube",
        y="nome",
        orientation="h",
        title="Ranking dos 10 Maiores Artilheiros",
        text="gols_clube", color="pais", hover_data={ "posicao":True, "clube":True, "pais":False}, labels={ "gols_clube": "Gols no Clube", "nome": "", "pais": "Seleção" }
    )
    

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

# 3 - Top Assistências

def grafico_top_assistencias(df):

    dados = (
        df.sort_values("assistencias_clube", ascending=False)
        .head(10)
    )

    fig = px.bar(
        dados,
        x="assistencias_clube",
        y="nome",
        orientation="h",
        title="Ranking dos 10 Maiores Assistentes",
        text="assistencias_clube"
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

# 4 - Distribuição das Idades

def grafico_idades(df):

    fig = px.histogram(
        df,
        x="idade",
        nbins=10,
        color="posicao",
        title="Distribuição dos Jogadores por Faixa Etária"
    )

    st.plotly_chart(fig, use_container_width=True)

# 5 - Clubes com mais jogadores

def grafico_clubes(df):

    dados = (
        df.groupby("clube")
        .size()
        .reset_index(name="Quantidade")
        .sort_values("Quantidade", ascending=False)
        .head(10)
    )

    fig = px.bar(
        dados,
        x="clube",
        y="Quantidade",
        color="Quantidade",
        title="Clubes com Maior Número de Jogadores Convocados"
    )

    st.plotly_chart(fig, use_container_width=True)

# 6 - Desempenho Médio da Seleção

def grafico_desempenho_selecao(df):

    selecao = st.selectbox(
        "Selecione uma seleção",
        sorted(df["pais"].unique()),
        key="desempenho_selecao",
        label_visibility="collapsed",
    )

    dados = df[df["pais"] == selecao]

    atributos = {
        "Ritmo": dados["ritmo"].mean(),
        "Finalização": dados["finalizacao"].mean(),
        "Passe": dados["passe"].mean(),
        "Drible": dados["drible"].mean(),
        "Defesa": dados["defesa"].mean(),
        "Físico": dados["fisico"].mean(),
    }

    fig = px.line_polar(
        r=list(atributos.values()),
        theta=list(atributos.keys()),
        line_close=True,
        title=f"Desempenho Médio da Seleção - {selecao}"
    )

    fig.update_traces(fill="toself")

    fig.update_layout(
        template="plotly_white",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="grafico_desempenho_selecao"
    )


# 7 - Média de Gols por Posição

def grafico_media_gols_posicao(df):

    dados = (
        df.groupby("posicao")["gols_clube"]
        .mean()
        .reset_index()
        .sort_values("gols_clube", ascending=False)
    )

    fig = px.bar(
        dados,
        x="gols_clube",
        y="posicao",
        orientation="h",
        text="gols_clube",
        title="Média de Gols por Posição",
        labels={
            "gols_clube": "Média de Gols",
            "posicao": "Posição"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        showlegend=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="grafico_media_gols_posicao"
    )