import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

class RAGSystem:
    def __init__(self, data_path=None):
        # 1. SMART PATH: Find the 'data' folder relative to where this script is saved
        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_path = os.path.join(base_dir, "data")
        else:
            self.data_path = data_path

        # 2. AUTO-CREATE: Create the folder if it doesn't exist
        os.makedirs(self.data_path, exist_ok=True)

        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.docs = []
        self.index = None

        # 3. LOAD & INDEX
        self.load_documents()
        self.create_index()

    def load_documents(self):
        files = [f for f in os.listdir(self.data_path) if os.path.isfile(os.path.join(self.data_path, f))]
        
        # Safety: If folder is empty, add a default message so it doesn't crash
        if not files:
            self.docs = ["The data folder is currently empty. Please add .txt files to the data directory."]
            return

        for file in files:
            with open(os.path.join(self.data_path, file), "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip(): # Only add if file isn't empty
                    chunks = self.chunk_text(text)
                    self.docs.extend(chunks)

    def chunk_text(self, text, chunk_size=300):
        words = text.split()
        return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    def create_index(self):
        # If no docs were loaded, we can't create a real index
        if not self.docs:
            self.docs = ["No content available."]
            
        embeddings = self.model.encode(self.docs)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype('float32'))

    def retrieve(self, query, k=3):
        q_embed = self.model.encode([query])
        distances, indices = self.index.search(np.array(q_embed).astype('float32'), k)

        # Filter out invalid indices
        results = [self.docs[i] for i in indices[0] if i < len(self.docs)]
        return results

    def generate_answer(self, context, query):
        prompt = f"""
        You are a helpful AI assistant.
        Answer the question using ONLY the context below.
        Context:
        {context}
        Question:
        {query}
        Answer clearly:
        """
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120 # Add a timeout so it doesn't hang forever
            )
            return response.json().get("response", "Error: No response from AI model.")
        except Exception as e:
            return f"⚠️ Connection Error: Is Ollama running? ({str(e)})"

    def ask(self, query):
        context_chunks = self.retrieve(query)
        context = "\n".join(context_chunks)
        answer = self.generate_answer(context, query)
        return answer, context_chunks

from dotenv import load_dotenv
load_dotenv()