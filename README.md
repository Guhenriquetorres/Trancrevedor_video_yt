# Transcritor & Analisador de Vídeos do YouTube

Este projeto transforma vídeos do YouTube em texto, realiza análise exploratória de palavras (EDA), gera nuvem de palavras e **avalia o sentimento do conteúdo**, tudo de forma automática.  
Inclui duas versões: **local (com transcrição automática via Whisper)** e **nuvem (análise pronta via Streamlit Cloud)**.

---

## 📂 Estrutura do Projeto

- `Analise_sent_streamlit.py` → Rodar LOCALMENTE (com transcrição automática via Whisper + análise de sentimento)
- `View_cloud_st.py` → Rodar na NUvem (Streamlit Cloud), onde você cola ou faz upload do texto transcrito
- `requirements.txt` → Lista de dependências para ambos ambientes
- `README.md` → (este arquivo!)

---

## **Como Usar Localmente** (transcrição automática)

### **1. Pré-requisitos**

- Python 3.8+
- Instale os pacotes com:

    ```bash
    pip install -r requirements.txt
    ```

- Tenha o [FFmpeg](https://ffmpeg.org/download.html) instalado no sistema (necessário para yt-dlp e Whisper).
    - No Windows: baixe e adicione o executável ao PATH.

### **2. Execute o app local**
- Use o script:

- Cole o link de um vídeo do YouTube no campo indicado e clique em **Analisar Vídeo**.

**Funcionalidades:**
- Baixa o áudio do vídeo do YouTube (`yt-dlp`)
- Transcreve usando **Whisper** (modelo local)
- Faz análise de palavras, gera gráficos, wordcloud e calcula o **sentimento** do texto com Hugging Face

---

##  **Como Usar na Nuvem (Streamlit Cloud)**

### **1. Faça deploy no [Streamlit Cloud](https://share.streamlit.io/)**
- Suba o repositório para o GitHub com o arquivo `requirements.txt` (como está).
- Use o script `View_cloud_st.py` ou outro arquivo onde o usuário **cola o texto transcrito**.

### **2. O que muda na nuvem**
- **A transcrição automática NÃO funciona na nuvem gratuita!**  
→ Por limitações de ffmpeg, yt-dlp e Whisper (não são suportados/no resource para rodar).
- Você pode:  
- **Colar o texto transcrito** manualmente na interface  
- (Opcional) Permitir upload de arquivo `.txt` com a transcrição

**Funcionalidades:**
- Faz toda a análise exploratória e de sentimento do texto, igual à versão local

---

## **Sobre o Whisper (OpenAI)**
- **Whisper** é um modelo open source da OpenAI para transcrição automática de áudio para texto.
- Ele pode ser rodado localmente (necessita baixar modelo, usar CPU ou GPU).
- Modelos disponíveis: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"` — quanto maior, mais preciso e lento.
- No código local, usamos `whisper.load_model("base")`, que equilibra precisão e velocidade.

---

## **Sobre o Modelo de Análise de Sentimento**
- Usamos o modelo **`nlptown/bert-base-multilingual-uncased-sentiment`** do [Hugging Face](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment).
- É um modelo BERT treinado para detectar sentimento em textos em **vários idiomas**, incluindo português.
- A saída é uma nota de 1 a 5 estrelas (`label`), onde:
  - **1 ou 2 stars:** negativo
  - **3 stars:** neutro
  - **4 ou 5 stars:** positivo

---

##  **Dependências**

Confira o arquivo `requirements.txt`:


