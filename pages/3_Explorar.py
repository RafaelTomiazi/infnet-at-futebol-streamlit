import pandas as pd
import folium
import pydeck as pdk
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(page_title="Explorar", page_icon="⚽", layout="wide")
st.title("⚽ Explorar")

st.write(
    "Deixei essa página pra reunir umas coisas a mais: um formulário, o upload de arquivo e "
    "um mapa. Não precisa ter escolhido partida pra usar."
)

st.header("Formulário")
with st.form("meu_form"):
    nome = st.text_input("Seu nome")
    time_favorito = st.selectbox("Time favorito", ["Nenhum", "Palmeiras", "Flamengo", "Corinthians", "Outro"])
    quantos = st.number_input("Quantos jogos por semana você assiste?", min_value=0, max_value=20, value=2)
    data = st.date_input("Data de hoje")
    hora = st.time_input("Horário que você costuma ver jogo")
    cor = st.color_picker("Escolha uma cor", "#1f77b4")
    comentario = st.text_area("Deixa um comentário sobre o dashboard")
    prefere = st.radio("Você prefere ver o que?", ["Passes", "Chutes"], horizontal=True)
    marcar = st.checkbox("Quero receber novidades")
    enviou = st.form_submit_button("Enviar")

if enviou:
    st.success(f"Valeu, {nome or 'visitante'}! Anotado.")
    st.balloons()
    st.write({
        "nome": nome,
        "time": time_favorito,
        "jogos_por_semana": quantos,
        "data": str(data),
        "hora": str(hora),
        "cor": cor,
        "comentario": comentario,
        "prefere": prefere,
        "novidades": marcar,
    })

st.header("Upload de arquivo")
arquivo = st.file_uploader("Suba um CSV, JSON ou imagem", type=["csv", "json", "png", "jpg"])
if arquivo is not None:
    if arquivo.name.endswith((".png", ".jpg")):
        st.image(arquivo, caption=arquivo.name, width=400)
    else:
        df = pd.read_csv(arquivo) if arquivo.name.endswith(".csv") else pd.read_json(arquivo)
        st.write("Primeiras linhas do arquivo:")
        st.dataframe(df.head())

# mapa com pydeck, como os eventos nao tem lat/long usei uns
# estadios famosos so pra mostrar a visualizacao espacial funcionando
st.header("Mapa de estádios (PyDeck)")
estadios = pd.DataFrame({
    "estadio": ["Maracanã", "Wembley", "Camp Nou", "Allianz Arena", "Santiago Bernabéu"],
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

# pensei em ficar so no pydeck mas quis testar o folium tambem, nele da pra clicar no marcador
st.header("Mesmo mapa com Folium")
mapa = folium.Map(location=[30, 0], zoom_start=2)
for _, e in estadios.iterrows():
    folium.CircleMarker([e["lat"], e["lon"]], radius=8, color="red", fill=True,
                        popup=e["estadio"]).add_to(mapa)
st_folium(mapa, height=400, use_container_width=True)
