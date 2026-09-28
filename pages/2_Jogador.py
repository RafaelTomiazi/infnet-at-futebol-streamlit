import streamlit as st

import graficos
import utils

st.set_page_config(page_title="Jogador", page_icon="⚽", layout="wide")
st.title("⚽ Análise por jogador")

if "match_id" not in st.session_state:
    st.warning("Escolha uma partida primeiro na página 'Partida'.")
    st.stop()

st.caption(f"Partida: {st.session_state.get('confronto', '')}")

with st.spinner("Carregando eventos..."):
    eventos = utils.separar_xy(utils.carregar_eventos(st.session_state["match_id"]))

jogadores = sorted(eventos["player"].dropna().unique().tolist())
salvo = st.session_state.get("jogador")
jogador = st.sidebar.selectbox("Jogador", jogadores,
                               index=jogadores.index(salvo) if salvo in jogadores else 0)
st.session_state["jogador"] = jogador

do_jogador = eventos[eventos["player"] == jogador]
passes = do_jogador[do_jogador["type"] == "Pass"]
passes_certos = passes[passes["pass_outcome"].isna()]
chutes = do_jogador[do_jogador["type"] == "Shot"]
gols = chutes[chutes["shot_outcome"] == "Goal"]
aproveitamento = (len(passes_certos) / len(passes) * 100) if len(passes) > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Passes certos", len(passes_certos), delta=f"de {len(passes)}", border=True)
c2.metric("Aproveitamento de passe", f"{aproveitamento:.0f}%", border=True)
c3.metric("Gols", len(gols), border=True)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Passes")
    st.pyplot(graficos.mapa_passes(passes, figsize=(7, 4.5)))
    st.caption("Azul = passe certo, vermelho = passe errado.")
with col_b:
    st.subheader("Onde ele atuou no campo")
    com_posicao = do_jogador.dropna(subset=["x", "y"])
    if len(com_posicao) > 2:
        st.pyplot(graficos.mapa_calor(com_posicao))
        st.caption("Número de ações em cada parte do campo (ataque pra direita).")
    else:
        st.info("Poucas ações desse jogador pra desenhar o mapa de calor.")

colunas = [c for c in ["minute", "type", "team", "player", "x", "y"] if c in do_jogador.columns]
st.download_button("Baixar ações do jogador em CSV",
                   do_jogador[colunas].to_csv(index=False).encode("utf-8"),
                   "acoes_jogador.csv", "text/csv")

st.header("Comparar dois jogadores")
with st.form("comparar"):
    a = st.selectbox("Jogador 1", jogadores, index=jogadores.index(jogador))
    b = st.selectbox("Jogador 2", jogadores, index=1 if len(jogadores) > 1 else 0)
    comparar = st.form_submit_button("Comparar")

if comparar:
    resumo = utils.resumo_jogadores(eventos)
    comparacao = resumo[resumo["player"].isin([a, b])].set_index("player")
    # magic do streamlit, a variavel sozinha na linha ja aparece na tela
    comparacao
    st.bar_chart(comparacao[["passes", "chutes", "gols"]].T)
