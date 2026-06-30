import streamlit as st

from utils.carregar_dados import carregar_dados
from utils.filtros import aplicar_filtros
from utils.KPIs import mostrar_kpis

from utils.graficos import (
    grafico_posicoes,
    grafico_top_gols,
    grafico_top_assistencias,
    grafico_idades,
    grafico_clubes,
    grafico_media_gols_posicao,
    grafico_desempenho_selecao,
)

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Dashboard Copa do Mundo 2026",
    page_icon="🏆",
    layout="wide"
)

# CABEÇALHO

st.title("🏆 Dashboard Analítico - Copa do Mundo 2026")
st.markdown("""Dashboard desenvolvido para a disciplina de **Banco de Dados II**.""")

st.info(
    """
    **Bases de dados utilizadas:**
    - `jogadores_selecoes_.csv` — informações dos jogadores (nome, posição, idade, clube, gols, assistências, atributos etc.).
    - `teams.csv` — informações das seleções (grupo, código FIFA e demais dados utilizados na integração).
    """
)

st.divider()

# CARREGAR DADOS

df = carregar_dados()

# FILTROS

df = aplicar_filtros(df)

# KPIs

mostrar_kpis(df)

st.markdown("<br>", unsafe_allow_html=True)

# PERFIL DOS JOGADORES

col1, col2 = st.columns(2, gap="large")

with col1:
    grafico_posicoes(df)

with col2:
    grafico_idades(df)

st.markdown("<br>", unsafe_allow_html=True)

# DESEMPENHO OFENSIVO

col3, col4 = st.columns(2, gap="large")

with col3:
    grafico_top_gols(df)

with col4:
    grafico_top_assistencias(df)

st.markdown("<br>", unsafe_allow_html=True)

# CLUBES

st.markdown("<br>", unsafe_allow_html=True)

grafico_clubes(df)

# SELEÇÕES - MEDIA GOLS POSIÇÃO

col5, col6, = st.columns(2, gap="large")

with col5:
    grafico_media_gols_posicao(df)

with col6:
    grafico_desempenho_selecao(df)
    
# TABELA

st.subheader("Tabela de Dados dos Jogadores")

colunas = [
    "nome",
    "pais",
    "posicao",
    "idade",
    "clube",
    "gols_clube",
    "assistencias_clube",
    "partidas_clube",
]

st.dataframe(
    df[colunas],
    use_container_width=True,
    hide_index=True
)

# RODAPÉ

st.markdown("---")

st.caption(
    """Projeto Final - Banco de Dados II
    IFNMG Campus Almenara
    Dashboard desenvolvido em Streamlit."""
)
