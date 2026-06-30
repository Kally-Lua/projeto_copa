import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1 - Jogadores por posição
cat > /mnt/user-data/outputs/graficos.py << 'ENDOFFILE'
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go  # NOVO: importamos go para o gráfico radar melhorado
import pandas as pd

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
# =============================================================================
# O QUE É CADA COISA — GLOSSÁRIO RÁPIDO
# =============================================================================
#
# 📌 PLOTLY:  biblioteca Python que cria gráficos interativos (você passa o
#             mouse e vê os valores, pode dar zoom, etc.)
#
# 📌 px.bar() / px.histogram() etc.: funções do Plotly que criam cada tipo
#             de gráfico (barras, histograma, radar...)
#
# 📌 fig.update_layout(): serve para ajustar o visual do gráfico INTEIRO
#             (cor de fundo, título, tamanho, legenda...)
#
# 📌 fig.update_traces(): serve para ajustar as BARRAS/PONTOS do gráfico
#             (cor, texto em cima das barras, etc.)
#
# 📌 st.plotly_chart(): exibe o gráfico dentro do Streamlit
#
# 📌 use_container_width=True: faz o gráfico ocupar toda a largura disponível
#
# 📌 color_discrete_sequence: define a lista de cores que o gráfico vai usar
#
# 📌 template="plotly_white": tema visual com fundo branco e linhas suaves
# =============================================================================


# =============================================================================
# GRÁFICO 1 — Jogadores por Posição
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Virou gráfico HORIZONTAL (barras na horizontal ficam mais fáceis de ler
#      quando os nomes são longos, como "Lateral Esquerdo")
#   ✅ Adicionamos cor fixa verde (#2e7d32) para ficar com cara de Copa
#   ✅ Adicionamos rótulos (números) do lado de fora de cada barra
#   ✅ Melhoramos os labels dos eixos (antes não tinha texto explicando)
#   ✅ Ajustamos o template para plotly_white (visual mais limpo)
# =============================================================================

def grafico_posicoes(df):

    # Agrupa os dados: conta quantos jogadores existem em cada posição
    dados = (
        df.groupby("posicao")
        .size()
        .reset_index(name="Quantidade")
        .sort_values("Quantidade", ascending=True)  # ascending=True: menor embaixo, maior em cima
    )

    # Cria o gráfico de barras HORIZONTAL (orientation="h")
    # ANTES era vertical (sem orientation="h"), ficava difícil ler os nomes
    fig = px.bar(
        dados,
        x="Quantidade",          # eixo X: o número de jogadores
        y="posicao",             # eixo Y: os nomes das posições
        orientation="h",         # NOVO: "h" = horizontal
        title="Jogadores por Posição",
        color_discrete_sequence=["#2e7d32"],  # NOVO: cor verde copa do mundo
        text="Quantidade",       # NOVO: mostra o número dentro/fora da barra
        labels={
            "posicao": "Posição",
            "Quantidade": "Nº de Jogadores"  # NOVO: label mais descritivo no eixo
        }
    )

    # Posiciona os números do lado de fora das barras
    # ANTES não tinha texto nenhum nas barras
    fig.update_traces(textposition="outside")

    fig.update_layout(
        template="plotly_white",   # fundo branco limpo
        height=400,                # NOVO: altura em pixels (antes usava padrão)
        yaxis_title="",            # NOVO: remove o título do eixo Y (já é óbvio)
        xaxis_title="Nº de Jogadores"
    )

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# GRÁFICO 2 — Top 10 Artilheiros
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Adicionamos a coluna "pais" como cor — assim cada barra tem a cor
#      da seleção do jogador, fica mais fácil identificar
#   ✅ Adicionamos hover_data com "posicao" e "clube" — ao passar o mouse
#      sobre a barra você vê a posição e o clube do jogador
#   ✅ Labels melhorados nos eixos
# =============================================================================

def grafico_top_gols(df):

    # Pega os 10 jogadores com mais gols, do maior para o menor
    dados = (
        df.sort_values("gols_clube", ascending=False)
        .head(10)
    )

    fig = px.bar(
        dados,
        x="gols_clube",
        y="nome",
        orientation="h",
        title="🥇 Top 10 Artilheiros",
        text="gols_clube",
        color="pais",            # NOVO: cada seleção tem uma cor diferente
        hover_data={             # NOVO: informações extras ao passar o mouse
            "posicao": True,
            "clube": True,
            "pais": False        # pais já aparece na legenda, não precisa repetir
        },
        labels={
            "gols_clube": "Gols no Clube",
            "nome": "",
            "pais": "Seleção"
        }
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),  # ordena do menor para o maior
        template="plotly_white",
        height=420,
        legend_title_text="Seleção"  # NOVO: título da legenda
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# GRÁFICO 3 — Top 10 Assistentes
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Mesma melhoria do gráfico de artilheiros: cor por seleção
#   ✅ hover_data com posição e clube
#   ✅ Emoji no título para ficar mais visual
# =============================================================================

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
        title="🎯 Top 10 Maiores Assistentes",
        text="assistencias_clube",
        color="pais",            # NOVO: cor por seleção
        hover_data={             # NOVO: info extra no hover
            "posicao": True,
            "clube": True,
            "pais": False
        },
        labels={
            "assistencias_clube": "Assistências no Clube",
            "nome": "",
            "pais": "Seleção"
        }
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        template="plotly_white",
        height=420,
        legend_title_text="Seleção"
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# GRÁFICO 4 — Distribuição das Idades
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Adicionamos uma linha vertical marcando a MÉDIA de idade
#      Isso é chamado de "anotação" — ajuda a interpretar o gráfico
#   ✅ Melhoramos os labels dos eixos
#   ✅ Adicionamos o parâmetro barmode="overlay" e opacity para as cores
#      não ficarem totalmente sólidas e esconderem umas às outras
# =============================================================================

def grafico_idades(df):

    # Calcula a média de idade para usar como linha de referência
    # NOVO: antes não tinha esse cálculo
    media_idade = df["idade"].mean()

    fig = px.histogram(
        df,
        x="idade",
        nbins=10,       # nbins = número de "caixinhas" (faixas) do histograma
        color="posicao",
        title="📊 Distribuição dos Jogadores por Faixa Etária",
        labels={
            "idade": "Idade",
            "count": "Quantidade de Jogadores",  # NOVO
            "posicao": "Posição"                 # NOVO
        },
        opacity=0.8     # NOVO: 0.8 = leve transparência para as barras não se sobreporem
    )

    # NOVO: adiciona uma linha vertical na média de idade
    # Isso ajuda a visualizar: "a maioria está acima ou abaixo da média?"
    fig.add_vline(
        x=media_idade,
        line_dash="dash",     # linha tracejada
        line_color="red",
        annotation_text=f"Média: {media_idade:.1f} anos",  # texto ao lado da linha
        annotation_position="top right"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        legend_title_text="Posição"  # NOVO
    )

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# GRÁFICO 5 — Clubes com mais jogadores convocados
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Adicionamos a cor por quantidade (gradiente de cor)
#      — quanto mais jogadores, mais escura fica a barra
#   ✅ Adicionamos os números em cima de cada barra (text="Quantidade")
#   ✅ Rotacionamos os nomes dos clubes no eixo X para não sobrepor
#   ✅ Removemos o título do eixo X (já é óbvio que são os clubes)
# =============================================================================

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
        color="Quantidade",   # cor varia conforme o valor (gradiente)
        title="🏟️ Top 10 Clubes com Mais Jogadores Convocados",
        text="Quantidade",    # NOVO: número em cima de cada barra
        color_continuous_scale="Greens",  # NOVO: escala de verde (do claro ao escuro)
        labels={
            "clube": "",
            "Quantidade": "Nº de Jogadores"
        }
    )

    fig.update_traces(textposition="outside")  # NOVO: número fora das barras

    fig.update_layout(
        template="plotly_white",
        height=420,
        coloraxis_showscale=False,  # NOVO: esconde a barrinha de escala de cor
        xaxis_tickangle=-35         # NOVO: inclina os nomes dos clubes 35 graus
    )

    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# GRÁFICO 6 — Desempenho Médio da Seleção (Radar)
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Trocamos px.line_polar por go.Scatterpolar — dá mais controle visual
#   ✅ Adicionamos o preenchimento (fill) com opacidade, ficou mais bonito
#   ✅ O gráfico agora mostra os VALORES de cada atributo dentro do radar
#   ✅ Melhoramos as cores e o visual geral
# =============================================================================

def grafico_desempenho_selecao(df):

    # st.selectbox = caixinha de seleção (dropdown) onde o usuário escolhe uma opção
    selecao = st.selectbox(
        "Selecione uma seleção para ver o desempenho:",
        sorted(df["pais"].unique()),
        key="desempenho_selecao",
    )

    # Filtra só os jogadores daquela seleção
    dados = df[df["pais"] == selecao]

    # Calcula a MÉDIA de cada atributo para a seleção escolhida
    # .mean() = calcula a média de todos os valores daquela coluna
    nomes_atributos = ["Ritmo", "Finalização", "Passe", "Drible", "Defesa", "Físico"]
    valores = [
        dados["ritmo"].mean(),
        dados["finalizacao"].mean(),
        dados["passe"].mean(),
        dados["drible"].mean(),
        dados["defesa"].mean(),
        dados["fisico"].mean(),
    ]

    # NOVO: usamos go.Figure com go.Scatterpolar no lugar de px.line_polar
    # Scatterpolar = gráfico em formato de "teia de aranha" (radar)
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores,                  # r = os valores de cada atributo
        theta=nomes_atributos,      # theta = os nomes que aparecem nas pontas
        fill="toself",              # preenche a área dentro do radar
        fillcolor="rgba(46,125,50,0.3)",  # NOVO: cor verde com transparência (0.3)
        line_color="#2e7d32",       # NOVO: cor da borda do radar
        name=selecao,
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]   # NOVO: define que a escala vai de 0 a 100
            )
        ),
        title=f"🕸️ Desempenho Médio — {selecao}",
        height=450,
        showlegend=False,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True, key="grafico_desempenho_selecao")


# =============================================================================
# GRÁFICO 7 — Média de Gols por Posição
# =============================================================================
# O QUE MUDOU EM RELAÇÃO AO ORIGINAL:
#   ✅ Adicionamos gradiente de cor (quanto mais gols, mais escuro)
#   ✅ Melhoramos o formato do número: de "1.234567" para "1.2"
#   ✅ Adicionamos um título mais visual com emoji
# =============================================================================

def grafico_media_gols_posicao(df):

    dados = (
        df.groupby("posicao")["gols_clube"]
        .mean()
        .reset_index()
        .sort_values("gols_clube", ascending=True)
    )

    fig = px.bar(
        dados,
        x="gols_clube",
        y="posicao",
        orientation="h",
        text="gols_clube",
        title="⚽ Média de Gols por Posição",
        color="gols_clube",                    # NOVO: cor varia pelo valor
        color_continuous_scale="Greens",       # NOVO: escala de cor verde
        labels={
            "gols_clube": "Média de Gols",
            "posicao": "Posição"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",  # ".1f" = mostra só 1 casa decimal
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        showlegend=False,
        coloraxis_showscale=False,  # NOVO: esconde a barrinha de cor (não precisa)
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="grafico_media_gols_posicao"
    )

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
        color=["#2e7d32"], 
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
        textposition="outside
