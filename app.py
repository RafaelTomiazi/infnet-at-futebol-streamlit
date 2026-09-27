# Dashboard de futebol - AT de Front-End com Python (Streamlit)
# Rafael Celestino Tomiazi - Infnet
# rodar com: streamlit run app.py

import streamlit as st

st.set_page_config(page_title="Dashboard de Futebol", page_icon="⚽", layout="wide")

st.title("⚽ Dashboard de Futebol")
st.caption("AT de Desenvolvimento Front-End com Python (Streamlit) - Infnet")

st.header("Sobre o projeto")
st.write(
    "A ideia aqui foi tentar responder uma pergunta que eu sempre fico pensando vendo jogo: quem "
    "realmente construiu o jogo e quem finalizou? So o placar nao mostra muito isso, entao fui "
    "atras dos dados de passe e de chute pra ver melhor como a partida foi."
)
st.write(
    "Os dados sao os abertos da StatsBomb, que tem evento por evento de varios jogos de verdade "
    "(tem Copa do Mundo, Bundesliga, etc). Nas outras paginas da pra escolher o jogo e ver os mapas "
    "e depois olhar um jogador especifico."
)

st.markdown(
    "Pra navegar e so usar o menu do lado: em **Partida** voce escolhe o campeonato e o jogo, em "
    "**Jogador** ve os numeros de um jogador daquela partida e em **Explorar** deixei o formulario, "
    "o upload e uns mapas."
)

st.header("Por que usei Streamlit")
st.write(
    "Escolhi o Streamlit porque da pra fazer um site so com Python, sem ter que mexer com HTML, CSS "
    "ou JavaScript. Como to indo mais pro lado de dados isso ajudou bastante, consegui focar na "
    "analise. Uma coisa que eu so entendi fazendo: toda vez que mexe num filtro ele roda o script "
    "inteiro de novo. Por isso usei cache pros dados da StatsBomb, senao ficava baixando tudo toda hora."
)

st.subheader("E os outros frameworks?")
st.write(
    "Dei uma olhada no Dash, no Panel e no Voila tambem. O Dash da mais liberdade no layout mas precisa "
    "escrever bem mais codigo com callbacks. O Panel e bom se ja usa muito o ecossistema PyData mas "
    "achei mais dificil de comecar. O Voila transforma um notebook em app, so que ai fica preso no "
    "formato do notebook. Pra um dashboard simples como esse o Streamlit foi o mais rapido."
)

st.header("Como rodar")
st.write("Criei um venv pra nao misturar as bibliotecas com o resto do pc e instalei tudo pelo requirements.txt:")
st.code(
    "python -m venv venv\n"
    "venv\\Scripts\\activate\n"
    "pip install -r requirements.txt\n"
    "streamlit run app.py",
    language="bash",
)
st.write("O codigo ta no GitHub e o deploy foi feito no Streamlit Community Cloud.")

st.info("Abre o menu do lado pra ir pras outras paginas 👈")
