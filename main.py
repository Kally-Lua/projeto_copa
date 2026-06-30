import streamlit as st

from utils.carregar_dados import carregar_dados
from utils.filtros import aplicar_filtros
from utils.KPIs import mostrar_kpis
from utils.graficos import utils.graficos

# CONFIGURAÇÃO DA PÁGINA

st.set_page_config(
    page_title="Copa do Mundo Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Parte de CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0a1628; }

/* menu da lateral */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2137 0%, #0a3d1f 100%);
}
section[data-testid="stSidebar"] * { color: #e8f5e9 !important; }

/* Configuração do layout*/
h1, h2, h3 { color: #f9c93e !important; }
p, label, .stMarkdown { color: #e0e0e0 !important; }

/* Configurando os KPIs */
.kpi-card {
    background: linear-gradient(135deg, #0d2137 0%, #1a3a2e 100%);
    border: 1px solid #2e7d32;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.25);
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f9c93e;
    margin: 4px 0;
}
.kpi-label {
    font-size: 0.85rem;
    color: #a5d6a7;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.kpi-icon { font-size: 1.6rem; }

/* Cabeçalho do dashboard */
.dashboard-header {
    background: linear-gradient(135deg, #0d4520 0%, #1b5e20 50%, #0d3a1a 100%);
    border: 1px solid #388e3c;
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    text-align: center;
}
.dashboard-header h1 { font-size: 2.5rem !important; margin: 0 !important; }
.dashboard-header p { color: #c8e6c9 !important; font-size: 1.05rem; margin-top: 6px; }

/* Abas */
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #a5d6a7 !important;
    border-bottom: 2px solid transparent;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    color: #f9c93e !important;
    border-bottom: 2px solid #f9c93e !important;
}

/* Foto do jogador */
/*.player-card {
    background: #0d2137;
    border: 1px solid #2e7d32;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.player-card img { border-radius: 8px; max-width: 100%; }
.player-name { font-size: 1.1rem; font-weight: 700; color: #f9c93e; margin-top: 8px; }
.player-info { font-size: 0.85rem; color: #a5d6a7; }
*/
/* Separador */
hr { border-color: #2e7d32 !important; opacity: 0.4; }
</style>
""", unsafe_allow_html=True)

# ── Cores padrão por seleção ────────────────────────────────────────────────
CORES_PAISES = {
    "Brasil":     "#009c3b",
    "Argentina":  "#74acdf",
    "França":     "#002395",
    "Portugal":   "#e42518",
    "Espanha":    "#c60b1e",
    "Alemanha":   "#000000",
    "Inglaterra": "#cf081f",
    "Itália":     "#0066b2",
    "Holanda":    "#ff6600",
    "Bélgica":    "#ed2939",
    "Croácia":    "#d31f31",
    "Uruguai":    "#5EB6E4",
    "Marrocos":   "#c1272d",
}

PALETA = [
    "#f9c93e", "#2e7d32", "#1565c0", "#e53935",
    "#8e24aa", "#00838f", "#ef6c00", "#558b2f",
    "#ad1457", "#00695c", "#283593", "#6d4c41",
]

# ── Carrega dados ───────────────────────────────────────────────────────────
df_raw = carregar_dados()


# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <h1>⚽ Copa do Mundo — Análise de Jogadores</h1>
    <p>Explore estatísticas e desempenho das principais seleções do mundo</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPIs
# ══════════════════════════════════════════════════════════════════════════════
#total_jogadores = len(df)
total_selecoes  = df["pais"].nunique()
idade_media     = round(pd.to_numeric(df["idade"], errors="coerce").mean(), 1)
total_gols      = int(pd.to_numeric(df["gols_clube"], errors="coerce").fillna(0).sum())
total_partidas  = int(pd.to_numeric(df["partidas_clube"], errors="coerce").fillna(0).sum())

k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, "👥", total_jogadores, "Jogadores"),
    (k2, "🌍", total_selecoes,  "Seleções"),
    (k3, "🎂", idade_media,     "Idade Média"),
    (k4, "⚽", total_gols,      "Gols Totais"),
    (k5, "🏃", total_partidas,  "Partidas"),
]
for col, icon, val, label in kpis:
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{val}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ABAS
# ══════════════════════════════════════════════════════════════════════════════

st.divider()


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
