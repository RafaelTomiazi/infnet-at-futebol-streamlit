# pagina que analisa uma partida: estatisticas, mapa de passes e mapa de chutes
import time

import streamlit as st

import graficos
import utils

st.set_page_config(page_title="Partida", page_icon="⚽", layout="wide")


def indice_salvo(opcoes, chave):
    # quando voltava pra essa pagina o selectbox voltava pro primeiro item
    # entao guardo a escolha no session_state e uso ela como index
    salvo = st.session_state.get(chave)
    return opcoes.index(salvo) if salvo in opcoes else 0


def barra_lateral():
    st.sidebar.header("Escolha a partida")

    with st.spinner("Carregando competicoes..."):
        competicoes = utils.carregar_competicoes().copy()
    competicoes["nome"] = competicoes["competition_name"] + " - " + competicoes["season_name"]
    nomes = competicoes["nome"].tolist()
    nome_comp = st.sidebar.selectbox("Campeonato e temporada", nomes,
                                     index=indice_salvo(nomes, "comp_nome"))
    st.session_state["comp_nome"] = nome_comp
    linha_comp = competicoes[competicoes["nome"] == nome_comp].iloc[0]

    with st.spinner("Carregando partidas..."):
        partidas = utils.carregar_partidas(int(linha_comp["competition_id"]),
                                           int(linha_comp["season_id"])).copy()
    partidas["confronto"] = (
        partidas["home_team"] + " x " + partidas["away_team"]
        + " (" + partidas["home_score"].astype(str) + "-" + partidas["away_score"].astype(str) + ")"
    )
    confrontos = partidas["confronto"].tolist()
    confronto = st.sidebar.selectbox("Partida", confrontos, index=indice_salvo(confrontos, "confronto"))
    linha_partida = partidas[partidas["confronto"] == confronto].iloc[0]

    # a pagina do jogador usa essas mesmas escolhas
    st.session_state["confronto"] = confronto
    st.session_state["match_id"] = int(linha_partida["match_id"])
    return nome_comp, linha_partida


def baixar_eventos(match_id):
    barra = st.progress(0, text="Baixando eventos da partida...")
    for i in range(0, 100, 25):
        time.sleep(0.1)
        barra.progress(i + 25, text="Baixando eventos da partida...")
    eventos = utils.carregar_eventos(match_id)
    barra.empty()
    return utils.separar_xy(eventos)


def mostrar_metricas(stats):
    taxa = (stats["gols"] / stats["chutes"] * 100) if stats["chutes"] > 0 else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Gols", stats["gols"], border=True)
    c2.metric("Chutes", stats["chutes"], border=True)
    c3.metric("Passes", stats["passes"], delta=f"{stats['passes_certos']} certos", border=True)
    # o delta verde destaca a taxa de conversao, que e o numero que mais me interessa
    c4.metric("Conversao", f"{taxa:.1f}%", delta=f"{stats['gols']} gols", border=True)
    st.latex(r"\text{Conversao} = \frac{\text{gols}}{\text{chutes}} \times 100")


def aba_mapas(eventos, times):
    time_escolhido = st.radio("Time", times, horizontal=True)
    col_passe, col_chute = st.columns(2)
    with col_passe:
        st.markdown("**Mapa de passes**")
        passes = eventos[(eventos["type"] == "Pass") & (eventos["team"] == time_escolhido)]
        st.pyplot(graficos.mapa_passes(passes))
        st.caption("Azul = passe certo, vermelho = passe errado.")
    with col_chute:
        st.markdown("**Mapa de chutes**")
        chutes = eventos[(eventos["type"] == "Shot") & (eventos["team"] == time_escolhido)]
        st.pyplot(graficos.mapa_chutes(chutes))
        st.caption("Estrela verde = gol. Tamanho do ponto = chance de gol (xG).")


def aba_graficos(eventos):
    passes_time = eventos[eventos["type"] == "Pass"].groupby("team").size().reset_index(name="passes")
    chutes_time = eventos[eventos["type"] == "Shot"].groupby("team").size().reset_index(name="chutes")

    st.markdown("**Passes acumulados ao longo do jogo**")
    # grafico nativo do streamlit, mostra qual time teve mais a bola em cada momento
    st.line_chart(utils.passes_acumulados(eventos))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Divisao dos passes (rosca)**")
        st.plotly_chart(graficos.grafico_pizza(passes_time))
    with col2:
        st.markdown("**Passes e chutes por time (subplots)**")
        st.plotly_chart(graficos.subplots_times(passes_time, chutes_time))

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Tipos de evento na partida (Altair)**")
        st.altair_chart(graficos.barras_tipos(eventos))
    with col4:
        st.markdown("**Tamanho dos passes por jogador (boxplot)**")
        st.altair_chart(graficos.boxplot_passes(eventos[eventos["type"] == "Pass"]))

    st.markdown("**Quem passa mais tambem chuta mais? (Seaborn)**")
    st.pyplot(graficos.relacao_passes_chutes(utils.resumo_jogadores(eventos)))


def aba_dados(eventos, stats):
    colunas = [c for c in ["minute", "type", "team", "player", "x", "y"] if c in eventos.columns]
    jogadores = ["Todos"] + sorted(eventos["player"].dropna().unique().tolist())

    # usei form pra nao recarregar a tabela a cada clique, so quando aplicar
    with st.form("filtros"):
        c1, c2 = st.columns(2)
        tipos = c1.multiselect("Tipos de evento", sorted(eventos["type"].unique()),
                               default=["Pass", "Shot"])
        jogador = c2.selectbox("Jogador", jogadores)
        minutos = st.slider("Intervalo de tempo (minutos)", 0, int(eventos["minute"].max()),
                            (0, int(eventos["minute"].max())))
        qtd = st.number_input("Quantidade de eventos pra mostrar", 5, 5000, 200)
        st.form_submit_button("Aplicar filtros")

    filtrado = eventos[eventos["minute"].between(minutos[0], minutos[1])]
    if tipos:
        filtrado = filtrado[filtrado["type"].isin(tipos)]
    if jogador != "Todos":
        filtrado = filtrado[filtrado["player"] == jogador]

    st.write(f"{len(filtrado)} eventos encontrados, mostrando ate {qtd}.")
    st.dataframe(filtrado[colunas].head(int(qtd)), height=300)
    st.download_button("Baixar eventos filtrados em CSV",
                       filtrado[colunas].to_csv(index=False).encode("utf-8"),
                       "eventos_partida.csv", "text/csv")

    st.markdown("**Resumo**")
    st.table({
        "Metrica": ["Gols", "Chutes", "Passes", "Passes certos"],
        "Valor": [stats["gols"], stats["chutes"], stats["passes"], stats["passes_certos"]],
    })

    with st.expander("Exemplo de evento em JSON"):
        # so pra deixar claro o formato bruto que vem da StatsBomb
        primeiro = {k: str(v) for k, v in eventos.iloc[0].dropna().to_dict().items()}
        st.json(primeiro)
        st.code('from statsbombpy import sb\neventos = sb.events(match_id=' + str(eventos["match_id"].iloc[0])
                + ')', language="python")


st.title("⚽ Analise da partida")
nome_comp, linha_partida = barra_lateral()
eventos = baixar_eventos(st.session_state["match_id"])
times = eventos["team"].dropna().unique().tolist()
stats = utils.estatisticas_partida(eventos)

st.subheader(st.session_state["confronto"])
st.caption(f"{nome_comp} | data: {linha_partida['match_date']}")
st.text(f"Estadio: {linha_partida.get('stadium', '-')}   |   Arbitro: {linha_partida.get('referee', '-')}")

mostrar_metricas(stats)

# separei as visualizacoes em abas pra pagina nao ficar rolando sem fim
t1, t2, t3 = st.tabs(["Mapas de campo", "Graficos", "Dados"])
with t1:
    aba_mapas(eventos, times)
with t2:
    aba_graficos(eventos)
with t3:
    aba_dados(eventos, stats)
