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
    "realmente construiu o jogo e quem finalizou? Só o placar não mostra muito isso, então fui "
    "atrás dos dados de passe e de chute pra ver melhor como a partida foi."
)
st.write(
    "Os dados são os abertos da StatsBomb, que tem evento por evento de vários jogos de verdade "
    "(tem Copa do Mundo, Bundesliga, etc). Nas outras páginas dá pra escolher o jogo e ver os mapas "
    "e depois olhar um jogador específico."
)

st.markdown(
    "Pra navegar é só usar o menu do lado: em **Partida** você escolhe o campeonato e o jogo, em "
    "**Jogador** vê os números de um jogador daquela partida e em **Explorar** deixei o formulário, "
    "o upload e uns mapas."
)

st.header("Por que usei Streamlit")
st.write(
    "Escolhi o Streamlit porque dá pra fazer um site só com Python, sem ter que mexer com HTML, CSS "
    "ou JavaScript. Como to indo mais pro lado de dados isso ajudou bastante, consegui focar na "
    "análise. Uma coisa que eu só entendi fazendo: toda vez que mexe num filtro ele roda o script "
    "inteiro de novo. Por isso usei cache pros dados da StatsBomb, senão ficava baixando tudo toda hora."
)

st.subheader("E os outros frameworks?")
st.write(
    "Dei uma olhada no Dash, no Panel e no Voila também. O Dash dá mais liberdade no layout mas precisa "
    "escrever bem mais código com callbacks. O Panel é bom se já usa muito o ecossistema PyData mas "
    "achei mais difícil de começar. O Voila transforma um notebook em app, só que aí fica preso no "
    "formato do notebook. Pra um dashboard simples como esse o Streamlit foi o mais rápido."
)

st.header("Como rodar")
st.write("Criei um venv pra não misturar as bibliotecas com o resto do pc e instalei tudo pelo requirements.txt:")
st.code(
    "python -m venv venv\n"
    "venv\\Scripts\\activate\n"
    "pip install -r requirements.txt\n"
    "streamlit run app.py",
    language="bash",
)
st.write("O código tá no GitHub e o deploy foi feito no Streamlit Community Cloud.")

st.info("Abre o menu do lado pra ir pras outras páginas 👈")
