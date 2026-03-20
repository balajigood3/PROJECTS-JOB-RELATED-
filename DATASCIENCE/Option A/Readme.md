# Mini RAG Telegram Bot

## Features
- Telegram bot interface
- Retrieval-Augmented Generation (RAG)
- Local embeddings using SentenceTransformers
- FAISS vector search
- Local LLM using Ollama (Mistral)

## Setup

1. Install dependencies:
pip install -r requirements.txt

2. Run Ollama:
ollama run mistral

3. Add your Telegram bot token in app.py

4. Run:
python app.py

## Usage
/ask <question>

## Architecture
User → Telegram → RAG → FAISS → Ollama → Response