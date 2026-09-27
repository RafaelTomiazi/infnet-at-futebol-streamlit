# pagina que olha um jogador especifico dentro da partida escolhida.
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

import utils

st.set_page_config(page_title="Jogador", page_icon="⚽", layout="wide")
st.title("⚽ Analise por jogador")

# essa pagina depende da partida escolhida la na aba Partida
if "match_id" not in st.session_state:
    st.warning("Escolha uma partida primeiro na pagina 'Partida'.")
    st.stop()

match_id = st.session_state["match_id"]
st.caption(f"Partida: {st.session_state.get('confronto', '')}")

with st.spinner("Carregando eventos..."):
    eventos = utils.separar_xy(utils.carregar_eventos(match_id))

jogadores = sorted(eventos["player"].dropna().unique().tolist())
jogador = st.sidebar.selectbox("Jogador", jogadores)

do_jogador = eventos[eventos["player"] == jogador]

# numeros do jogador
passes = do_jogador[do_jogador["type"] == "Pass"]
passes_certos = passes[passes["pass_outcome"].isna()]
chutes = do_jogador[do_jogador["type"] == "Shot"]
gols = chutes[chutes["shot_outcome"] == "Goal"]
aproveitamento = (len(passes_certos) / len(passes) * 100) if len(passes) > 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Passes certos", len(passes_certos), delta=f"de {len(passes)}")
c2.metric("Aproveitamento de passe", f"{aproveitamento:.0f}%")
c3.metric("Gols", len(gols))

st.subheader(f"Passes de {jogador}")
# reaproveito o mesmo estilo de mapa da outra pagina, so que so pros passes desse jogador
campo = Pitch(pitch_type="statsbomb", line_color="black")
fig, ax = campo.draw(figsize=(7, 4.5))
for _, p in passes.iterrows():
    if isinstance(p["location"], list) and isinstance(p["pass_end_location"], list):
        cor = "red" if isinstance(p["pass_outcome"], str) else "blue"
        campo.arrows(p["location"][0], p["location"][1],
                     p["pass_end_location"][0], p["pass_end_location"][1],
                     ax=ax, color=cor, width=1, headwidth=4, alpha=0.6)
st.pyplot(fig)

# um grafico do seaborn pra ver onde no campo esse jogador mais tocou na bola
st.subheader("Onde ele atuou no campo")
com_posicao = do_jogador.dropna(subset=["x", "y"])
if len(com_posicao) > 2:
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    sns.kdeplot(data=com_posicao, x="x", y="y", fill=True, cmap="Reds", ax=ax2)
    ax2.set_xlim(0, 120)
    ax2.set_ylim(0, 80)
    ax2.set_xlabel("campo (ataque para a direita)")
    st.pyplot(fig2)
else:
    st.info("Poucas acoes desse jogador pra desenhar o mapa de calor.")

# download so das acoes do jogador
colunas = [c for c in ["minute", "type", "team", "player", "x", "y"] if c in do_jogador.columns]
st.download_button(
    "Baixar acoes do jogador em CSV",
    do_jogador[colunas].to_csv(index=False).encode("utf-8"),
    "acoes_jogador.csv",
    "text/csv",
)
