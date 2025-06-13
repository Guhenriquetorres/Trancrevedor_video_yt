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
        fig, ax = plt.subplots(figsize=(8, 5))
        df.head(20).plot.bar(x="Palavra", y="Frequência", color="#00cccc", legend=False, ax=ax, edgecolor="#1d4851")
        plt.xticks(rotation=45)
        ax.set_facecolor("#111920")
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("### ☁️ Nuvem de Palavras")
        wordcloud = WordCloud(
            width=800, height=400,
            background_color="#111920",
            colormap="cool",
            stopwords=stopwords_pt
        ).generate(" ".join(palavras_filtradas))
        fig_wc, ax_wc = plt.subplots(figsize=(10, 4))
        ax_wc.imshow(wordcloud, interpolation="bilinear")
        ax_wc.axis("off")
        fig_wc.patch.set_facecolor('#111920')
        st.pyplot(fig_wc)

    with col3:
        st.markdown("### 💬 Análise de Sentimento")
        texto_sent = texto[:512] if len(texto) > 512 else texto
        @st.cache_resource
        def get_classifier():
            return pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                framework="pt"
            )
        classifier = get_classifier()
        with st.spinner("Analisando sentimento..."):
            result = classifier(texto_sent)
            label = result[0]['label']
            score = result[0]['score']
            if "1" in label or "2" in label:
                st.error(f"Sentimento: {label} (Negativo)\nConfiança: {score:.2f}")
            elif "3" in label:
                st.warning(f"Sentimento: {label} (Neutro)\nConfiança: {score:.2f}")
            else:
                st.success(f"Sentimento: {label} (Positivo)\nConfiança: {score:.2f}")

    # Estatísticas básicas
    st.markdown("### 📈 Estatísticas Básicas")
    c1, c2, c3 = st.columns(3)
    media = np.mean(df["Frequência"])
    mediana = np.median(df["Frequência"])
    moda_valor = df["Frequência"].mode()[0]
    palavra_media = df.iloc[(df["Frequência"] - media).abs().idxmin()]["Palavra"]
    palavra_mediana = df.iloc[(df["Frequência"] - mediana).abs().idxmin()]["Palavra"]
    palavras_moda = df[df["Frequência"] == moda_valor]["Palavra"].tolist()
    c1.metric("Média", f"{media:.2f}", palavra_media)
    c2.metric("Mediana", f"{mediana}", palavra_mediana)
    c3.metric("Moda", f"{moda_valor}", ', '.join(palavras_moda))

    # Bigramas
    with st.expander("🔍 Bigramas mais frequentes"):
        def bigramas(lista):
            a, b = tee(lista)
            next(b, None)
            return zip(a, b)
        bigramas_mais_frequentes = Counter(bigramas(palavras_filtradas))
        df_bigramas = pd.DataFrame(bigramas_mais_frequentes.most_common(10), columns=["Bigramas", "Frequência"])
        st.table(df_bigramas)

    st.markdown("---")
    st.success(f"""
    💡 **Insights**  
    • Palavra mais frequente: **{df.iloc[0]['Palavra']}**  
    • Total de palavras únicas: **{df.shape[0]}**  
    • Frequência média: **{media:.2f}**  
    • A nuvem de palavras destaca os principais termos visualmente.
    """)
    st.markdown("---")
    st.subheader("📋 Tabela Completa de Palavras")
    st.dataframe(df, height=400, use_container_width=True)

else:
    st.info("Cole o texto transcrito acima para começar a análise!")

st.markdown("""
    <hr style='border-top: 1px solid #00cccc;'>
    <p style='text-align:center; color: #888; font-size:14px;'>
        Powered by <b>Streamlit</b> + <b>Hugging Face</b> | por @guhenriqutorres
    </p>
""", unsafe_allow_html=True)
