# Dashboard de Futebol - AT (Streamlit)

Rafael Celestino Tomiazi - Infnet

Dashboard de sports analytics feito em Streamlit. A pergunta que ele responde e:
numa partida, quem construiu o jogo e quem finalizou? Pra isso uso os dados abertos
da StatsBomb (evento por evento de partidas reais) e desenho os mapas de passe e de
chute com o mplsoccer.

## Paginas
- **app.py** - pagina inicial, com a explicacao do projeto e do Streamlit
- **pages/1_Partida.py** - estatisticas, mapa de passes e de chutes, graficos e dados da partida
- **pages/2_Jogador.py** - analise de um jogador (passes, aproveitamento, mapa de calor)
- **pages/3_Explorar.py** - formulario, upload de arquivo e mapa com PyDeck e Folium
- **utils.py** - funcoes que carregam os dados (com cache)
- **graficos.py** - funcoes que montam os graficos
- **hello.py** - primeiro teste do ambiente

## Como rodar

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Se der `No module named 'mplsoccer'` e porque o streamlit rodou fora do venv. Da pra rodar direto com
`.\venv\Scripts\python.exe -m streamlit run app.py`

Os dados vem da internet pela StatsBombPy, entao precisa estar conectado. O primeiro
carregamento demora um pouco porque baixa os eventos; depois o cache deixa rapido.
