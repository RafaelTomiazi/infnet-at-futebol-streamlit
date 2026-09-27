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
    # location vem como lista [x, y], separo em duas colunas pros graficos
    df = eventos.copy()
    df["x"] = df["location"].apply(lambda v: v[0] if isinstance(v, list) else None)
    df["y"] = df["location"].apply(lambda v: v[1] if isinstance(v, list) else None)
    return df


def estatisticas_partida(eventos):
    passes = eventos[eventos["type"] == "Pass"]
    chutes = eventos[eventos["type"] == "Shot"]
    # detalhe do StatsBomb, quando o passe da certo o pass_outcome fica vazio
    passes_certos = passes[passes["pass_outcome"].isna()]
    gols = chutes[chutes["shot_outcome"] == "Goal"]
    return {
        "passes": len(passes),
        "passes_certos": len(passes_certos),
        "chutes": len(chutes),
        "gols": len(gols),
    }


def resumo_jogadores(eventos):
    df = eventos.dropna(subset=["player"])
    resumo = df.groupby(["player", "team"]).agg(
        passes=("type", lambda t: (t == "Pass").sum()),
        chutes=("type", lambda t: (t == "Shot").sum()),
    ).reset_index()
    gols = df[df["shot_outcome"] == "Goal"].groupby("player").size()
    resumo["gols"] = resumo["player"].map(gols).fillna(0).astype(int)
    return resumo


def passes_acumulados(eventos):
    passes = eventos[eventos["type"] == "Pass"]
    tabela = passes.groupby(["minute", "team"]).size().unstack(fill_value=0)
    return tabela.cumsum()
