import streamlit as st
import pandas as pd


def mostrar_kpis(df):
    """Exibe os principais indicadores do dashboard."""
    # Indicadores

    total_jogadores = len(df)

    idade_media = round(
        pd.to_numeric(df["idade"], errors="coerce").mean(),
        1
    )

    total_gols = int(
        pd.to_numeric(df["gols_clube"], errors="coerce")
        .fillna(0)
        .sum()
    )

    total_partidas = int(
        pd.to_numeric(df["partidas_clube"], errors="coerce")
        .fillna(0)
        .sum()
    )

    total_paises = df["pais"].nunique()

    # Exibição

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "👥 Total de Jogadores",
            total_jogadores
        )

    with col2:
        st.metric(
            "🌍 Total de Seleções",
            total_paises
        )

    with col3:
        st.metric(
            "🎂 Idade Média",
            idade_media
        )

    with col4:
        st.metric(
            "⚽ Total de Gols",
            total_gols
        )

    with col5:
        st.metric(
            "🏃 Total dePartidas",
            total_partidas
        )