import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():

    # CSV dos jogadores
    jogadores = pd.read_csv("dados/jogadores_selecoes_.csv")

    # CSV das seleções
    teams = pd.read_csv("dados/teams.csv")

    # Traduzir nomes das seleções para inglês
    # (para combinar com o teams.csv)

    traducao = {
        "Brasil": "Brazil",
        "Argentina": "Argentina",
        "França": "France",
        "Portugal": "Portugal",
        "Espanha": "Spain",
        "Alemanha": "Germany",
        "Inglaterra": "England",
        "Itália": "Italy",
        "Holanda": "Netherlands",
        "Bélgica": "Belgium",
        "Croácia": "Croatia",
        "Uruguai": "Uruguay",
        "México": "Mexico",
        "Estados Unidos": "United States",
        "Canadá": "Canada",
        "Japão": "Japan",
        "Coreia do Sul": "South Korea",
        "Marrocos": "Morocco",
        "Senegal": "Senegal",
        "Camarões": "Cameroon",
        "Suíça": "Switzerland",
        "Dinamarca": "Denmark",
        "Polônia": "Poland",
        "Sérvia": "Serbia",
        "Austrália": "Australia",
        "Irã": "Iran",
        "Arábia Saudita": "Saudi Arabia",
        "Costa Rica": "Costa Rica",
        "Gana": "Ghana",
        "Tunísia": "Tunisia",
        "Equador": "Ecuador",
        "Catar": "Qatar"
    }

    jogadores["team_name"] = jogadores["pais"].replace(traducao)

    # Merge das duas bases

    df = jogadores.merge(
        teams,
        on="team_name",
        how="left"
    )

    return df