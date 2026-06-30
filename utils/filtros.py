import streamlit as st


def aplicar_filtros(df):
    """Aplica os filtros do dashboard."""

    st.sidebar.title("Filtros")

    # Seleção

    paises = sorted(df["pais"].dropna().unique())

    pais = st.sidebar.selectbox(
        "Seleção",
        options=["Todas"] + paises,
        index=0
    )

    # Posição

    posicoes = sorted(df["posicao"].dropna().unique())

    posicao = st.sidebar.multiselect(
        "Posição",
        options=posicoes,
        placeholder="Selecione uma ou mais posições"
    )

    # Aplicação dos filtros

    df_filtrado = df.copy()

    if pais != "Todas":
        df_filtrado = df_filtrado[df_filtrado["pais"] == pais]

    if posicao:
        df_filtrado = df_filtrado[
            df_filtrado["posicao"].isin(posicao)
        ]
        
    return df_filtrado