# pagina que analisa uma partida: estatisticas, mapa de passes e mapa de chutes.
import time

import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from mplsoccer import Pitch
from plotly.subplots import make_subplots

import utils

st.set_page_config(page_title="Partida", page_icon="⚽", layout="wide")
st.title("⚽ Analise da partida")

# selecao na barra lateral
st.sidebar.header("Escolha a partida")

with st.spinner("Carregando competicoes..."):
    competicoes = utils.carregar_competicoes()

competicoes = competicoes.copy()
competicoes["nome"] = competicoes["competition_name"] + " - " + competicoes["season_name"]
nome_comp = st.sidebar.selectbox("Campeonato e temporada", competicoes["nome"].tolist())
linha_comp = competicoes[competicoes["nome"] == nome_comp].iloc[0]

with st.spinner("Carregando partidas..."):
    partidas = utils.carregar_partidas(int(linha_comp["competition_id"]), int(linha_comp["season_id"]))

partidas = partidas.copy()
partidas["confronto"] = (
    partidas["home_team"] + " x " + partidas["away_team"]
    + " (" + partidas["home_score"].astype(str) + "-" + partidas["away_score"].astype(str) + ")"
)
confronto = st.sidebar.selectbox("Partida", partidas["confronto"].tolist())
linha_partida = partidas[partidas["confronto"] == confronto].iloc[0]
match_id = int(linha_partida["match_id"])

# guardo a partida no session_state pra pagina do jogador usar a mesma escolha
st.session_state["match_id"] = match_id
st.session_state["confronto"] = confronto

# barra de progresso enquanto baixa os eventos
barra = st.progress(0, text="Baixando eventos da partida...")
for i in range(0, 100, 25):
    time.sleep(0.1)
    barra.progress(i + 25, text="Baixando eventos da partida...")
eventos = utils.carregar_eventos(match_id)
barra.empty()

eventos = utils.separar_xy(eventos)
times = eventos["team"].dropna().unique().tolist()

st.subheader(confronto)
st.caption(f"{nome_comp} | data: {linha_partida['match_date']}")

# metricas basicas
stats = utils.estatisticas_partida(eventos)
taxa = (stats["gols"] / stats["chutes"] * 100) if stats["chutes"] > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Gols", stats["gols"])
c2.metric("Chutes", stats["chutes"])
c3.metric("Passes", stats["passes"])
# o delta verde destaca a taxa de conversao, que e o numero que mais me interessa
c4.metric("Conversao", f"{taxa:.1f}%", delta=f"{stats['gols']} gols")

st.latex(r"\text{Conversao} = \frac{\text{gols}}{\text{chutes}} \times 100")

# separei as visualizacoes em abas pra pagina nao ficar rolando sem fim
aba_campo, aba_graficos, aba_dados = st.tabs(["Mapas de campo", "Graficos", "Dados"])

with aba_campo:
    time_escolhido = st.radio("Time", times, horizontal=True)
    col_passe, col_chute = st.columns(2)

    with col_passe:
        st.markdown("**Mapa de passes**")
        passes = eventos[(eventos["type"] == "Pass") & (eventos["team"] == time_escolhido)]
        campo = Pitch(pitch_type="statsbomb", line_color="black")
        fig, ax = campo.draw(figsize=(6, 4))
        for _, p in passes.iterrows():
            if isinstance(p["location"], list) and isinstance(p["pass_end_location"], list):
                # se pass_outcome tem texto o passe deu errado, senao deu certo
                cor = "red" if isinstance(p["pass_outcome"], str) else "blue"
                campo.arrows(p["location"][0], p["location"][1],
                             p["pass_end_location"][0], p["pass_end_location"][1],
                             ax=ax, color=cor, width=1, headwidth=4, alpha=0.5)
        st.pyplot(fig)
        st.caption("Azul = passe certo, vermelho = passe errado.")

    with col_chute:
        st.markdown("**Mapa de chutes**")
        chutes = eventos[(eventos["type"] == "Shot") & (eventos["team"] == time_escolhido)]
        campo2 = Pitch(pitch_type="statsbomb", line_color="black")
        fig2, ax2 = campo2.draw(figsize=(6, 4))
        for _, ch in chutes.iterrows():
            if isinstance(ch["location"], list):
                gol = ch["shot_outcome"] == "Goal"
                # deixo o tamanho do ponto pela chance de gol (xG), fica mais informativo
                tam = 100 * float(ch.get("shot_statsbomb_xg") or 0.05) + 30
                campo2.scatter(ch["location"][0], ch["location"][1], ax=ax2, s=tam,
                               color="green" if gol else "gray",
                               marker="*" if gol else "o", edgecolors="black", alpha=0.7)
        st.pyplot(fig2)
        st.caption("Estrela verde = gol. Tamanho do ponto = chance de gol (xG).")

with aba_graficos:
    passes_time = eventos[eventos["type"] == "Pass"].groupby("team").size().reset_index(name="passes")
    chutes_time = eventos[eventos["type"] == "Shot"].groupby("team").size().reset_index(name="chutes")

    st.markdown("**Passes por time (pizza)**")
    st.plotly_chart(px.pie(passes_time, names="team", values="passes"), use_container_width=True)

    st.markdown("**Passes e chutes por time (subplots)**")
    sub = make_subplots(rows=1, cols=2, subplot_titles=("Passes", "Chutes"))
    sub.add_trace(go.Bar(x=passes_time["team"], y=passes_time["passes"]), row=1, col=1)
    sub.add_trace(go.Bar(x=chutes_time["team"], y=chutes_time["chutes"]), row=1, col=2)
    sub.update_layout(height=350, showlegend=False)
    st.plotly_chart(sub, use_container_width=True)

    st.markdown("**Tipos de evento na partida (Altair)**")
    tipos = eventos["type"].value_counts().reset_index()
    tipos.columns = ["tipo", "quantidade"]
    grafico = (
        alt.Chart(tipos.head(10))
        .mark_bar()
        .encode(x="quantidade:Q", y=alt.Y("tipo:N", sort="-x"), tooltip=["tipo", "quantidade"])
        .properties(height=350)
    )
    st.altair_chart(grafico, use_container_width=True)

with aba_dados:
    st.markdown("**Eventos da partida**")
    colunas = [c for c in ["minute", "type", "team", "player", "x", "y"] if c in eventos.columns]
    st.dataframe(eventos[colunas], use_container_width=True, height=300)

    st.download_button(
        "Baixar eventos em CSV",
        eventos[colunas].to_csv(index=False).encode("utf-8"),
        "eventos_partida.csv",
        "text/csv",
    )

    st.markdown("**Resumo**")
    st.table({
        "Metrica": ["Gols", "Chutes", "Passes", "Passes certos"],
        "Valor": [stats["gols"], stats["chutes"], stats["passes"], stats["passes_certos"]],
    })

    # mostro um evento em JSON so pra deixar claro o formato bruto que vem da StatsBomb
    st.markdown("**Exemplo de evento em JSON**")
    primeiro = {k: str(v) for k, v in eventos.iloc[0].dropna().to_dict().items()}
    st.json(primeiro)
