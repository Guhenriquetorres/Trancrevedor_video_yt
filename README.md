# Transcrição e Análise de Sentimento de Vídeos do YouTube com Whisper (OpenAI) e Transformers

Este projeto permite baixar o áudio de vídeos do YouTube, transcrever automaticamente usando o modelo Whisper local (open source e gratuito), e analisar o sentimento do texto gerado usando modelos da Hugging Face.

## ⚡️ Funcionalidades

- Download de áudio de vídeos do YouTube (`yt-dlp`)
- Transcrição automática com Whisper local (OpenAI)
- Análise de sentimento do texto usando modelo BERT multilíngue da Hugging Face
- Tudo rodando localmente, sem custos com API

## 🚀 Requisitos

- Python 3.8+
- pip

## 🛠️ Instalação

1. **Clone o repositório ou copie os arquivos do projeto**

2. **Instale as dependências necessárias:**

```bash
pip install git+https://github.com/openai/whisper.git
pip install yt-dlp
pip install torch
pip install transformers
