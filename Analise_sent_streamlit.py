import streamlit as st
import os
import yt_dlp
import whisper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import string
from itertools import tee

st.set_page_config(page_title="Resumo e Análise de Vídeo do YouTube", layout="wide", page_icon="🎧")

st.markdown("""
    <h1 style='text-align: center; color: #1d4851;'>
         Resumo & Análise Automática de Vídeos do YouTube
    </h1>
    <p style='text-align: center; color: #00cccc; font-size:18px;'>
        Cole o link do vídeo, clique em <b>Analisar</b> e veja a transcrição, nuvem de palavras, sentimento e insights!
    </p>
    <hr style='border-top: 1px solid #00cccc;'>
""", unsafe_allow_html=True)

with st.container():
    st.write("")

url = st.text_input("🔗 Link do vídeo do YouTube:", "", placeholder="Cole aqui o link do vídeo")
iniciar = st.button(" Analisar Vídeo")

def baixar_audio_ytdlp(url, caminho_destino, nome_arquivo='audio'):
    os.makedirs(caminho_destino, exist_ok=True)
    caminho_completo = os.path.join(caminho_destino, nome_arquivo + '.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': caminho_completo,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir(caminho_destino):
        if file.startswith(nome_arquivo) and file.endswith('.mp3'):
            return os.path.join(caminho_destino, file)
    return None

@st.cache_resource
def carregar_whisper(modelo="base"):
    return whisper.load_model(modelo)

def transcrever_whisper_local(caminho_arquivo, modelo="base"):
    model = carregar_whisper(modelo)
    resultado = model.transcribe(caminho_arquivo)
    return resultado['text']

def processa_texto(texto):
    texto = texto.lower()
    for pontuacao in string.punctuation + "“”’‘–—…":
        texto = texto.replace(pontuacao, " ")
    palavras = texto.split()
    stopwords_pt = set(stopwords.words('portuguese'))
    palavras_filtradas = [p for p in palavras if p not in stopwords_pt and len(p) > 2]
    contagem = Counter(palavras_filtradas)
    df = pd.DataFrame(contagem.items(), columns=["Palavra", "Frequência"]).sort_values("Frequência", ascending=False)
    return texto, palavras_filtradas, df

@st.cache_resource
def get_classifier():
    from transformers import pipeline
    return pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment",
        framework="pt"
    )

if iniciar and url:
    with st.spinner("⏳ Baixando áudio e transcrevendo... Isso pode levar alguns minutos..."):
        pasta_destino = "audios_yt"
        nome = "audio_yt"
        caminho_audio = baixar_audio_ytdlp(url, pasta_destino, nome)
        texto = transcrever_whisper_local(caminho_audio, modelo="base")
        st.success("✅ Transcrição concluída!")

    st.markdown("---")
    st.markdown("<h3 style='color:#1d4851;'>📝 Transcrição do Áudio</h3>", unsafe_allow_html=True)
    st.text_area("Texto Transcrito", texto, height=180)

    texto_processado, palavras_filtradas, df = processa_texto(texto)

    col1, col2= st.columns([2, 2])

    with col1:
        st.markdown("### 📊 Top 20 Palavras Mais Frequentes")
        fig, ax = plt.subplots(figsize=(9, 5))
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
            stopwords=stopwords.words('portuguese')
        ).generate(" ".join(palavras_filtradas))
        fig_wc, ax_wc = plt.subplots(figsize=(11, 4))
        ax_wc.imshow(wordcloud, interpolation="bilinear")
        ax_wc.axis("off")
        fig_wc.patch.set_facecolor('#111920')
        st.pyplot(fig_wc)

    with st.container():
        st.markdown("### 💬 Análise de Sentimento")
        texto_sent = texto[:512] if len(texto) > 512 else texto
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
                
    with st.container():
        st.markdown("### 📈 Estatísticas Básicas")
        # Cards com stats
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
elif url:
    st.warning("Clique em **Analisar Vídeo** para iniciar o processamento!")
else:
    st.info("Cole o link do vídeo do YouTube acima e clique em **Analisar Vídeo**.")

st.markdown("""
    <hr style='border-top: 1px solid #00cccc;'>
    <p style='text-align:center; color: #888; font-size:14px;'>
        Powered by <b>Streamlit</b> + <b>OpenAI Whisper</b> + <b>yt-dlp</b> | por @guhenriqutorres
    </p>
""", unsafe_allow_html=True)
