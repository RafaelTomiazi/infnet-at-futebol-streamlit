# Dashboard de futebol - AT de Front-End com Python (Streamlit)
# Rafael Celestino Tomiazi - Infnet
# rodar com: streamlit run app.py

import streamlit as st

st.set_page_config(page_title="Dashboard de Futebol", page_icon="⚽", layout="wide")

st.title("⚽ Dashboard de Futebol - Sports Analytics")
st.caption("AT de Desenvolvimento Front-End com Python (Streamlit) - Infnet")

st.header("Sobre o projeto")
st.write(
    "A pergunta que eu quis responder com esse dashboard e simples: numa partida, quem "
    "construiu o jogo e quem finalizou? Normalmente a gente olha so o placar, mas os dados "
    "de passe e de chute mostram bem melhor como o jogo aconteceu de verdade."
)
st.write(
    "Uso os dados abertos da StatsBomb, que trazem evento por evento de partidas reais, "
    "inclusive de Copa do Mundo. Nas outras paginas da pra escolher a partida, ver o mapa de "
    "passes e de chutes e tambem analisar um jogador."
)

st.markdown(
    """
**Como navegar** (menu na barra lateral):

- **Partida** — escolhe campeonato, temporada e jogo e ve as estatisticas e os mapas de campo.
- **Jogador** — filtra por um jogador e ve os numeros dele.
- **Explorar** — formularios, upload de arquivo e uns graficos extras.
"""
)

st.header("Por que Streamlit")
st.write(
    "Escolhi o Streamlit porque ele deixa transformar um script Python em site sem eu precisar "
    "saber HTML, CSS ou JavaScript. Como estou indo pra area de dados, isso me ajuda muito: eu "
    "foco na analise e a biblioteca cuida da interface. Cada vez que mexo num filtro, o Streamlit "
    "roda o script inteiro de novo e redesenha a tela. E facil de entender, mas gasta processamento, "
    "e e por isso que o cache dos dados da StatsBomb faz tanta diferenca aqui."
)

st.subheader("Streamlit x outros frameworks")
# achei que uma tabela resolvia melhor essa comparacao do que um paragrafo corrido
st.markdown(
    """
| Ferramenta | Ponto forte | Limitacao |
|---|---|---|
| **Streamlit** | Rapido de escrever, otimo pra dashboard de dados | Menos controle fino do layout |
| **Dash** | Layout bem flexivel, bom pra app grande | Mais codigo e mais complexo |
| **Panel** | Combina bem com o ecossistema PyData | Curva de aprendizado maior |
| **Voila** | Transforma notebook Jupyter em app na hora | Preso ao formato de notebook |
"""
)
st.write(
    "Pra um trabalho de analise como esse, o Streamlit foi o mais direto. Dash e Panel fariam mais "
    "sentido num sistema maior, e o Voila se eu ja tivesse tudo pronto num notebook."
)

st.header("Ambiente e dependencias")
st.write(
    "Rodei o projeto num ambiente virtual (venv) pra nao misturar as bibliotecas com o resto do "
    "computador. As dependencias ficam no requirements.txt, que e o mesmo arquivo que o Streamlit "
    "Cloud usa no deploy."
)
st.code(
    "python -m venv venv\n"
    "venv\\Scripts\\activate        # no Windows\n"
    "pip install -r requirements.txt\n"
    "streamlit run app.py",
    language="bash",
)
st.write(
    "Pro controle de versao usei Git e GitHub, commitando as partes e dando push pro repositorio, "
    "que depois liguei ao Streamlit Cloud pra publicar."
)

st.info("Abre o menu na barra lateral pra navegar pelas paginas.")
