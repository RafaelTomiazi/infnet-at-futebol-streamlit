# pensei em deixar cada grafico dentro da sua pagina mas o mapa de passes ia ficar
# repetido nas duas, entao juntei os graficos aqui
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from mplsoccer import Pitch
from plotly.subplots import make_subplots


def mapa_passes(passes, figsize=(6, 4)):
    campo = Pitch(pitch_type="statsbomb", line_color="black")
    fig, ax = campo.draw(figsize=figsize)
    for _, p in passes.iterrows():
        if isinstance(p["location"], list) and isinstance(p["pass_end_location"], list):
            # se pass_outcome tem texto o passe deu errado, senao deu certo
            cor = "red" if isinstance(p["pass_outcome"], str) else "blue"
            campo.arrows(p["location"][0], p["location"][1],
                         p["pass_end_location"][0], p["pass_end_location"][1],
                         ax=ax, color=cor, width=1, headwidth=4, alpha=0.5)
    return fig


def mapa_chutes(chutes, figsize=(6, 4)):
    campo = Pitch(pitch_type="statsbomb", line_color="black")
    fig, ax = campo.draw(figsize=figsize)
    for _, ch in chutes.iterrows():
        if isinstance(ch["location"], list):
            gol = ch["shot_outcome"] == "Goal"
            # tamanho do ponto pelo xG
            xg = ch.get("shot_statsbomb_xg")
            tam = 100 * float(xg if xg == xg and xg is not None else 0.05) + 30
            campo.scatter(ch["location"][0], ch["location"][1], ax=ax, s=tam,
                          color="green" if gol else "gray",
                          marker="*" if gol else "o", edgecolors="black", alpha=0.7)
    return fig


def mapa_calor(acoes):
    # tinha feito com kdeplot do seaborn num grafico comum, mas o heatmap do
    # mplsoccer (tirei da galeria deles) ja desenha o campo por baixo e fica mais claro
    campo = Pitch(pitch_type="statsbomb", line_zorder=2, line_color="black")
    fig, ax = campo.draw(figsize=(7, 4.5))
    stats = campo.bin_statistic(acoes["x"], acoes["y"], statistic="count", bins=(6, 5))
    campo.heatmap(stats, ax=ax, cmap="Reds", edgecolors="white")
    campo.label_heatmap(stats, ax=ax, color="black", fontsize=10, ha="center", va="center",
                        str_format="{:.0f}")
    return fig


def grafico_pizza(passes_time):
    return px.pie(passes_time, names="team", values="passes", hole=0.4)


def subplots_times(passes_time, chutes_time):
    sub = make_subplots(rows=1, cols=2, subplot_titles=("Passes", "Chutes"))
    sub.add_trace(go.Bar(x=passes_time["team"], y=passes_time["passes"]), row=1, col=1)
    sub.add_trace(go.Bar(x=chutes_time["team"], y=chutes_time["chutes"]), row=1, col=2)
    sub.update_layout(height=350, showlegend=False)
    return sub


def barras_tipos(eventos):
    tipos = eventos["type"].value_counts().reset_index()
    tipos.columns = ["tipo", "quantidade"]
    return (
        alt.Chart(tipos.head(10))
        .mark_bar()
        .encode(x="quantidade:Q", y=alt.Y("tipo:N", sort="-x"), tooltip=["tipo", "quantidade"])
        .properties(height=350)
    )


def boxplot_passes(passes):
    top = passes["player"].value_counts().head(8).index
    dados = passes[passes["player"].isin(top)][["player", "pass_length"]]
    return (
        alt.Chart(dados)
        .mark_boxplot()
        .encode(x=alt.X("pass_length:Q", title="tamanho do passe"),
                y=alt.Y("player:N", title=None), color=alt.Color("player:N", legend=None))
        .properties(height=350)
    )


def relacao_passes_chutes(por_jogador):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=por_jogador, x="passes", y="chutes", hue="team", s=80, ax=ax)
    ax.set_title("Passes x chutes de cada jogador")
    return fig
