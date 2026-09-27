# funcoes que cuidam so dos dados. deixei elas aqui separadas pra nao poluir as
# paginas, que ai ficam so com a parte da tela.
import pandas as pd
import streamlit as st
from statsbombpy import sb


@st.cache_data(ttl=3600)
def carregar_competicoes():
    return sb.competitions()


@st.cache_data(ttl=3600)
def carregar_partidas(competition_id, season_id):
    return sb.matches(competition_id=competition_id, season_id=season_id)


# os eventos sao a parte pesada (uns 3 mil por jogo), por isso o cache aqui ajuda bastante
@st.cache_data(ttl=3600)
def carregar_eventos(match_id):
    return sb.events(match_id=match_id)


def separar_xy(eventos):
    # a coluna location vem como lista [x, y]. quase todo grafico precisa do x e y
    # separados, entao ja quebro em duas colunas aqui.
    df = eventos.copy()
    df["x"] = df["location"].apply(lambda v: v[0] if isinstance(v, list) else None)
    df["y"] = df["location"].apply(lambda v: v[1] if isinstance(v, list) else None)
    return df


def estatisticas_partida(eventos):
    passes = eventos[eventos["type"] == "Pass"]
    chutes = eventos[eventos["type"] == "Shot"]
    # detalhe do StatsBomb: quando o passe da certo, pass_outcome fica vazio
    passes_certos = passes[passes["pass_outcome"].isna()]
    gols = chutes[chutes["shot_outcome"] == "Goal"]
    return {
        "passes": len(passes),
        "passes_certos": len(passes_certos),
        "chutes": len(chutes),
        "gols": len(gols),
    }
