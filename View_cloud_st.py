import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import string
from itertools import tee

from transformers import pipeline

st.set_page_config(page_title="Resumo e Análise de Texto", layout="wide", page_icon="🎧")

st.markdown("""
    <h1 style='text-align: center; color: #1d4851;'>Resumo & Análise de Texto</h1>
    <p style='text-align: center; color: #00cccc; font-size:18px;'>
        Cole abaixo o texto transcrito do áudio do vídeo do YouTube.<br>
        Veja análise de sentimento, nuvem de palavras e estatísticas automáticas!
    </p>
    <hr style='border-top: 1px solid #00cccc;'>
""", unsafe_allow_html=True)

texto = st.text_area("Cole aqui o texto transcrito para analisar:", height=200)

if texto:
    # Processamento de texto
    texto_proc = texto.lower()
    for pontuacao in string.punctuation + "“”’‘–—…":
        texto_proc = texto_proc.replace(pontuacao, " ")
    palavras = texto_proc.split()
    stopwords_pt = set(stopwords.words('portuguese'))
    palavras_filtradas = [p for p in palavras if p not in stopwords_pt and len(p) > 2]
    contagem = Counter(palavras_filtradas)
    df = pd.DataFrame(contagem.items(), columns=["Palavra", "Frequência"]).sort_values("Frequência", ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📊 Top 20 Palavras Mais Frequentes")
        fig, ax = plt.subpl
