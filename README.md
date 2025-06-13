# 🎧 Transcritor & Analisador de Vídeos do YouTube

Este projeto transforma vídeos do YouTube em texto, realiza análise exploratória de palavras (EDA), gera nuvem de palavras e **avalia o sentimento do conteúdo**, tudo de forma automática.  
Inclui duas versões: **local (com transcrição automática via Whisper)** e **nuvem (análise pronta via Streamlit Cloud)**.

---

## 📂 Estrutura do Projeto

- `Analise_sent_streamlit.py` → Rodar LOCALMENTE (com transcrição automática via Whisper + análise de sentimento)
- `View_cloud_st.py` → Rodar na NUvem (Streamlit Cloud), onde você cola ou faz upload do texto transcrito
- `requirements.txt` → Lista de dependências para ambos ambientes
- `README.md` → (este arquivo!)

---

## 🚀 **Como Usar Localmente** (transcrição automática)

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
