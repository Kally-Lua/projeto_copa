"""
Dashboard - Copa do Mundo
Banco de Dados II - IFNMG Campus Almenara
Prof. Suzana Mota
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from carregar_dados.py import carregar_dados

# ── Configuração da página ──────────────────────────────────────────────────
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


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — FILTROS
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("## ⚽ Copa do Mundo")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtros")

# Filtro 1 — Seleção
paises_disp = sorted(df_raw["pais"].dropna().unique())
pais_sel = st.sidebar.selectbox(
    "🌍 Seleção",
    options=["Todas"] + paises_disp,
    index=0
)

# Filtro 2 — Posição
posicoes_disp = sorted(df_raw["posicao"].dropna().unique())
posicoes_sel = st.sidebar.multiselect(
    "📌 Posição",
    options=posicoes_disp,
    placeholder="Todas as posições"
)

# Filtro 3 — Faixa etária (bônus)
idade_min, idade_max = int(df_raw["idade"].min()), int(df_raw["idade"].max())
faixa_idade = st.sidebar.slider(
    "🎂 Faixa etária",
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max)
)

st.sidebar.markdown("---")
st.sidebar.info("📊 Dados: Copa do Mundo 2022\n\n🏫 IFNMG - BD2")

# ── Aplica filtros ──────────────────────────────────────────────────────────
df = df_raw.copy()
if pais_sel != "Todas":
    df = df[df["pais"] == pais_sel]
if posicoes_sel:
    df = df[df["posicao"].isin(posicoes_sel)]
df = df[(df["idade"] >= faixa_idade[0]) & (df["idade"] <= faixa_idade[1])]

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
total_jogadores = len(df)
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
aba1, aba2, aba3, aba4 = st.tabs([
    "📊 Visão Geral",
    "🏆 Rankings",
    "🕹️ Desempenho",
    "🔍 Jogadores"
])


# ══════════════════════════════════════════════════════════════════════════════
# ABA 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
with aba1:
    st.markdown("### Distribuição e Perfil dos Jogadores")

    col_a, col_b = st.columns(2)

    # ── Gráfico 1: Jogadores por Posição ────────────────────────────────────
    with col_a:
        dados_pos = (
            df.groupby("posicao")
            .size()
            .reset_index(name="Quantidade")
            .sort_values("Quantidade", ascending=True)
        )
        fig1 = px.bar(
            dados_pos,
            x="Quantidade",
            y="posicao",
            orientation="h",
            title="Jogadores por Posição",
            color="Quantidade",
            color_continuous_scale=["#1b5e20", "#f9c93e"],
            text="Quantidade",
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            yaxis_title="",
            xaxis_title="Quantidade de Jogadores",
            title_font_color="#f9c93e",
            height=380,
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ── Gráfico 2: Distribuição de Idades ───────────────────────────────────
    with col_b:
        fig2 = px.histogram(
            df,
            x="idade",
            nbins=12,
            color="posicao",
            title="Distribuição por Faixa Etária",
            color_discrete_sequence=PALETA,
            labels={"idade": "Idade", "count": "Jogadores", "posicao": "Posição"},
        )
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_font_color="#f9c93e",
            legend_title_text="Posição",
            height=380,
            bargap=0.05,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Gráfico 3: Jogadores por Seleção ────────────────────────────────────
    st.markdown("---")
    dados_pais = (
        df.groupby("pais")
        .size()
        .reset_index(name="Jogadores")
        .sort_values("Jogadores", ascending=False)
    )
    cores_barras = [CORES_PAISES.get(p, "#f9c93e") for p in dados_pais["pais"]]

    fig3 = go.Figure(go.Bar(
        x=dados_pais["pais"],
        y=dados_pais["Jogadores"],
        marker_color=cores_barras,
        text=dados_pais["Jogadores"],
        textposition="outside",
    ))
    fig3.update_layout(
        title="Jogadores Convocados por Seleção",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_color="#f9c93e",
        yaxis_title="Nº de Jogadores",
        xaxis_title="",
        height=360,
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ── Gráfico 4: Clubes com mais convocados ───────────────────────────────
    dados_clubes = (
        df.groupby("clube")
        .size()
        .reset_index(name="Quantidade")
        .sort_values("Quantidade", ascending=False)
        .head(10)
    )
    fig4 = px.bar(
        dados_clubes,
        x="clube",
        y="Quantidade",
        title="Top 10 Clubes com Mais Jogadores Convocados",
        color="Quantidade",
        color_continuous_scale=["#1b5e20", "#f9c93e"],
        text="Quantidade",
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        title_font_color="#f9c93e",
        xaxis_title="",
        height=380,
    )
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ABA 2 — RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with aba2:
    st.markdown("### Rankings de Desempenho Individual")

    col_r1, col_r2 = st.columns(2)

    # ── Gráfico 5: Top 10 Artilheiros ───────────────────────────────────────
    with col_r1:
        top_gols = (
            df.sort_values("gols_clube", ascending=False)
            .head(10)
        )
        fig5 = px.bar(
            top_gols,
            x="gols_clube",
            y="nome",
            orientation="h",
            title="🥇 Top 10 Artilheiros",
            color="pais",
            color_discrete_map=CORES_PAISES,
            text="gols_clube",
            labels={"gols_clube": "Gols", "nome": "", "pais": "Seleção"},
        )
        fig5.update_traces(textposition="outside")
        fig5.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(categoryorder="total ascending"),
            title_font_color="#f9c93e",
            height=400,
            showlegend=True,
            legend_title_text="Seleção",
        )
        st.plotly_chart(fig5, use_container_width=True)

    # ── Gráfico 6: Top 10 Assistentes ───────────────────────────────────────
    with col_r2:
        top_ass = (
            df.sort_values("assistencias_clube", ascending=False)
            .head(10)
        )
        fig6 = px.bar(
            top_ass,
            x="assistencias_clube",
            y="nome",
            orientation="h",
            title="🎯 Top 10 Assistentes",
            color="pais",
            color_discrete_map=CORES_PAISES,
            text="assistencias_clube",
            labels={"assistencias_clube": "Assistências", "nome": "", "pais": "Seleção"},
        )
        fig6.update_traces(textposition="outside")
        fig6.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(categoryorder="total ascending"),
            title_font_color="#f9c93e",
            height=400,
            showlegend=True,
            legend_title_text="Seleção",
        )
        st.plotly_chart(fig6, use_container_width=True)

    # ── Gráfico 7: Média de Gols por Posição ────────────────────────────────
    st.markdown("---")
    col_r3, col_r4 = st.columns(2)

    with col_r3:
        media_gols_pos = (
            df.groupby("posicao")["gols_clube"]
            .mean()
            .reset_index()
            .sort_values("gols_clube", ascending=True)
        )
        fig7 = px.bar(
            media_gols_pos,
            x="gols_clube",
            y="posicao",
            orientation="h",
            title="Média de Gols por Posição",
            color="gols_clube",
            color_continuous_scale=["#1b5e20", "#f9c93e"],
            text="gols_clube",
            labels={"gols_clube": "Média de Gols", "posicao": ""},
        )
        fig7.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig7.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            title_font_color="#f9c93e",
            height=380,
        )
        st.plotly_chart(fig7, use_container_width=True)

    # ── Gráfico 8: Scatter Gols x Assistências ──────────────────────────────
    with col_r4:
        fig8 = px.scatter(
            df,
            x="gols_clube",
            y="assistencias_clube",
            color="pais",
            size="partidas_clube",
            hover_name="nome",
            hover_data={"posicao": True, "clube": True},
            title="Gols vs Assistências (tamanho = partidas)",
            color_discrete_map=CORES_PAISES,
            labels={
                "gols_clube": "Gols no Clube",
                "assistencias_clube": "Assistências no Clube",
                "pais": "Seleção",
            },
        )
        fig8.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_font_color="#f9c93e",
            height=380,
            legend_title_text="Seleção",
        )
        st.plotly_chart(fig8, use_container_width=True)

    # ── Gráfico 9: Copas do mundo por jogador (top 10) ───────────────────────
    st.markdown("---")
    top_copas = (
        df.sort_values("num_copas", ascending=False)
        .head(12)[["nome", "pais", "num_copas", "idade"]]
    )
    fig9 = px.bar(
        top_copas,
        x="nome",
        y="num_copas",
        color="pais",
        color_discrete_map=CORES_PAISES,
        title="🌍 Jogadores com Mais Copas do Mundo Disputadas",
        text="num_copas",
        labels={"nome": "", "num_copas": "Nº de Copas", "pais": "Seleção"},
    )
    fig9.update_traces(textposition="outside")
    fig9.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_color="#f9c93e",
        height=380,
        legend_title_text="Seleção",
    )
    st.plotly_chart(fig9, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ABA 3 — DESEMPENHO (Radar + Heatmap)
# ══════════════════════════════════════════════════════════════════════════════
with aba3:
    st.markdown("### Análise de Desempenho das Seleções")

    col_d1, col_d2 = st.columns([1, 1])

    # ── Gráfico 10: Radar de Atributos por Seleção ──────────────────────────
    with col_d1:
        st.markdown("#### 🕸️ Radar de Atributos")
        selecao_radar = st.selectbox(
            "Selecione a seleção para o radar:",
            sorted(df_raw["pais"].unique()),
            key="sel_radar"
        )
        dados_radar = df_raw[df_raw["pais"] == selecao_radar]
        atributos = {
            "Ritmo":      dados_radar["ritmo"].mean(),
            "Finalização":dados_radar["finalizacao"].mean(),
            "Passe":      dados_radar["passe"].mean(),
            "Drible":     dados_radar["drible"].mean(),
            "Defesa":     dados_radar["defesa"].mean(),
            "Físico":     dados_radar["fisico"].mean(),
        }
        fig10 = go.Figure(go.Scatterpolar(
            r=list(atributos.values()),
            theta=list(atributos.keys()),
            fill="toself",
            name=selecao_radar,
            line_color=CORES_PAISES.get(selecao_radar, "#f9c93e"),
            fillcolor=CORES_PAISES.get(selecao_radar, "#f9c93e"),
            opacity=0.4,
        ))
        fig10.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    color="#a5d6a7", gridcolor="#2e7d32"
                ),
                angularaxis=dict(color="#f9c93e"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            title=f"Desempenho Médio — {selecao_radar}",
            title_font_color="#f9c93e",
            height=420,
            showlegend=False,
        )
        st.plotly_chart(fig10, use_container_width=True)

    # ── Gráfico 11: Comparativo de Atributos entre Seleções ─────────────────
    with col_d2:
        st.markdown("#### ⚡ Comparar Duas Seleções")
        paises_lista = sorted(df_raw["pais"].unique())
        s1 = st.selectbox("Seleção 1:", paises_lista, index=0, key="s1")
        s2 = st.selectbox("Seleção 2:", paises_lista, index=1, key="s2")

        atribs = ["ritmo", "finalizacao", "passe", "drible", "defesa", "fisico"]
        labels_atribs = ["Ritmo", "Finalização", "Passe", "Drible", "Defesa", "Físico"]

        med1 = df_raw[df_raw["pais"] == s1][atribs].mean().tolist()
        med2 = df_raw[df_raw["pais"] == s2][atribs].mean().tolist()

        fig11 = go.Figure()
        fig11.add_trace(go.Scatterpolar(
            r=med1 + [med1[0]],
            theta=labels_atribs + [labels_atribs[0]],
            fill="toself",
            name=s1,
            line_color=CORES_PAISES.get(s1, "#f9c93e"),
            opacity=0.5,
        ))
        fig11.add_trace(go.Scatterpolar(
            r=med2 + [med2[0]],
            theta=labels_atribs + [labels_atribs[0]],
            fill="toself",
            name=s2,
            line_color=CORES_PAISES.get(s2, "#1565c0"),
            opacity=0.5,
        ))
        fig11.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    color="#a5d6a7", gridcolor="#2e7d32"
                ),
                angularaxis=dict(color="#f9c93e"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            title=f"{s1}  vs  {s2}",
            title_font_color="#f9c93e",
            height=420,
            legend=dict(font=dict(color="#e0e0e0")),
        )
        st.plotly_chart(fig11, use_container_width=True)

    # ── Gráfico 12: Heatmap de Atributos Médios por Seleção ─────────────────
    st.markdown("---")
    st.markdown("#### 🔥 Heatmap de Atributos por Seleção")

    pivot = (
        df_raw.groupby("pais")[atribs]
        .mean()
        .rename(columns={
            "ritmo": "Ritmo", "finalizacao": "Finalização",
            "passe": "Passe", "drible": "Drible",
            "defesa": "Defesa", "fisico": "Físico"
        })
    )
    fig12 = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale="YlGn",
        aspect="auto",
        title="Média de Atributos por Seleção",
        labels={"color": "Valor"},
    )
    fig12.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_color="#f9c93e",
        font_color="#e0e0e0",
        height=420,
        xaxis_title="",
        yaxis_title="",
    )
    st.plotly_chart(fig12, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ABA 4 — JOGADORES (cards individuais)
# ══════════════════════════════════════════════════════════════════════════════
with aba4:
    st.markdown("### 🔍 Ficha Individual dos Jogadores")

    col_j1, col_j2 = st.columns([1, 2])

    with col_j1:
        pais_jogador = st.selectbox(
            "🌍 Seleção:", sorted(df_raw["pais"].unique()), key="pais_jogador"
        )
        nomes_disp = sorted(
            df_raw[df_raw["pais"] == pais_jogador]["nome"].tolist()
        )
        nome_jogador = st.selectbox("👤 Jogador:", nomes_disp, key="nome_jogador")

    jogador = df_raw[df_raw["nome"] == nome_jogador].iloc[0]

    with col_j1:
        # Foto
        if pd.notna(jogador.get("foto_url", None)) and str(jogador["foto_url"]).startswith("http"):
            st.image(jogador["foto_url"], use_container_width=True)

        st.markdown(f"""
        <div style="background:#0d2137;border:1px solid #2e7d32;border-radius:10px;padding:14px;margin-top:10px">
            <p style="color:#f9c93e;font-size:1.2rem;font-weight:700;margin:0">{jogador['nome']}</p>
            <p style="color:#a5d6a7;margin:4px 0">🌍 {jogador['pais']}</p>
            <p style="color:#a5d6a7;margin:4px 0">📌 {jogador['posicao']}</p>
            <p style="color:#a5d6a7;margin:4px 0">🎂 {int(jogador['idade'])} anos</p>
            <p style="color:#a5d6a7;margin:4px 0">🏟️ {jogador['clube']}</p>
            <p style="color:#a5d6a7;margin:4px 0">🌍 {int(jogador['num_copas'])} Copa(s)</p>
        </div>
        """, unsafe_allow_html=True)

    with col_j2:
        # KPIs do jogador
        kj1, kj2, kj3 = st.columns(3)
        kj1.metric("⚽ Gols", int(jogador["gols_clube"]))
        kj2.metric("🎯 Assistências", int(jogador["assistencias_clube"]))
        kj3.metric("🏃 Partidas", int(jogador["partidas_clube"]))

        st.markdown("<br>", unsafe_allow_html=True)

        # Radar individual
        atributos_jog = {
            "Ritmo":       jogador["ritmo"],
            "Finalização": jogador["finalizacao"],
            "Passe":       jogador["passe"],
            "Drible":      jogador["drible"],
            "Defesa":      jogador["defesa"],
            "Físico":      jogador["fisico"],
        }
        # média da seleção para comparação
        med_selecao = df_raw[df_raw["pais"] == jogador["pais"]][
            ["ritmo", "finalizacao", "passe", "drible", "defesa", "fisico"]
        ].mean()

        fig_jog = go.Figure()
        fig_jog.add_trace(go.Scatterpolar(
            r=list(atributos_jog.values()),
            theta=list(atributos_jog.keys()),
            fill="toself",
            name=nome_jogador,
            line_color="#f9c93e",
            fillcolor="#f9c93e",
            opacity=0.5,
        ))
        fig_jog.add_trace(go.Scatterpolar(
            r=med_selecao.tolist(),
            theta=list(atributos_jog.keys()),
            fill="toself",
            name=f"Média {jogador['pais']}",
            line_color=CORES_PAISES.get(jogador["pais"], "#2e7d32"),
            fillcolor=CORES_PAISES.get(jogador["pais"], "#2e7d32"),
            opacity=0.3,
            line_dash="dot",
        ))
        fig_jog.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    color="#a5d6a7", gridcolor="#2e7d32"
                ),
                angularaxis=dict(color="#f9c93e"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            title=f"Atributos: {nome_jogador} vs Média {jogador['pais']}",
            title_font_color="#f9c93e",
            height=380,
            legend=dict(font=dict(color="#e0e0e0")),
        )
        st.plotly_chart(fig_jog, use_container_width=True)

        # Barra de atributos
        df_atrib = pd.DataFrame({
            "Atributo": list(atributos_jog.keys()),
            "Valor":    list(atributos_jog.values()),
        })
        fig_bar_jog = px.bar(
            df_atrib,
            x="Atributo",
            y="Valor",
            color="Valor",
            color_continuous_scale=["#1b5e20", "#f9c93e"],
            title="Distribuição de Atributos",
            text="Valor",
            range_y=[0, 100],
        )
        fig_bar_jog.update_traces(textposition="outside")
        fig_bar_jog.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            title_font_color="#f9c93e",
            height=280,
            xaxis_title="",
        )
        st.plotly_chart(fig_bar_jog, use_container_width=True)

# ── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#4caf50;font-size:0.85rem'>"
    "⚽ Copa do Mundo Dashboard · Banco de Dados II · IFNMG Campus Almenara · Prof. Suzana Mota"
    "</p>",
    unsafe_allow_html=True
)
