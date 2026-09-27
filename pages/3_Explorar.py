# pagina mais solta: formularios, upload de arquivo e um mapa com pydeck.
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Explorar", page_icon="⚽", layout="wide")
st.title("⚽ Explorar")

st.write(
    "Deixei essa pagina pra reunir umas coisas a mais: um formulario, o upload de arquivo e "
    "um mapa. Nao precisa ter escolhido partida pra usar."
)

# formulario com varios tipos de campo. usei o st.form pra so processar quando clicar
st.header("Formulario")
with st.form("meu_form"):
    nome = st.text_input("Seu nome")
    time_favorito = st.selectbox("Time favorito", ["Nenhum", "Palmeiras", "Flamengo", "Corinthians", "Outro"])
    quantos = st.number_input("Quantos jogos por semana voce assiste?", min_value=0, max_value=20, value=2)
    data = st.date_input("Data de hoje")
    cor = st.color_picker("Escolha uma cor", "#1f77b4")
    prefere = st.radio("Voce prefere ver o que?", ["Passes", "Chutes"], horizontal=True)
    marcar = st.checkbox("Quero receber novidades")
    enviou = st.form_submit_button("Enviar")

if enviou:
    st.success(f"Valeu, {nome or 'visitante'}! Anotado.")
    # o st.write aceita varios tipos de uma vez, entao jogo o resumo como dicionario
    st.write({
        "nome": nome,
        "time": time_favorito,
        "jogos_por_semana": quantos,
        "data": str(data),
        "cor": cor,
        "prefere": prefere,
        "novidades": marcar,
    })

# upload de arquivo. a rubrica pede um servico de upload, entao aceito CSV e JSON
st.header("Upload de arquivo")
arquivo = st.file_uploader("Suba um CSV ou JSON pra dar uma olhada", type=["csv", "json"])
if arquivo is not None:
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_json(arquivo)
    st.write("Primeiras linhas do arquivo:")
    st.dataframe(df.head(), use_container_width=True)

# mapa com pydeck. como os eventos nao tem lat/long, usei as cidades-sede de uns
# estadios famosos so pra mostrar a visualizacao espacial funcionando.
st.header("Mapa de estadios (PyDeck)")
estadios = pd.DataFrame({
    "estadio": ["Maracana", "Wembley", "Camp Nou", "Allianz Arena", "Santiago Bernabeu"],
    "lat": [-22.912, 51.556, 41.380, 48.218, 40.453],
    "lon": [-43.230, -0.279, 2.122, 11.624, -3.688],
})
camada = pdk.Layer(
    "ScatterplotLayer",
    data=estadios,
    get_position=["lon", "lat"],
    get_radius=80000,
    get_fill_color=[200, 30, 30, 160],
    pickable=True,
)
st.pydeck_chart(pdk.Deck(
    layers=[camada],
    initial_view_state=pdk.ViewState(latitude=30, longitude=0, zoom=1.2),
    tooltip={"text": "{estadio}"},
))

st.balloons()
