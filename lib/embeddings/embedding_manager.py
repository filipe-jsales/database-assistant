import os
import requests
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import uuid

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")

collection_name = "message_embeddings"
collection = client.get_or_create_collection(collection_name)

def generate_embeddings(texts, model="llama3"):
    url = os.getenv("API_EMBEDDING_URL", "https://ollama.chargedcloud.com.br/api/embed")
    data = {
        "model": model,
        "input": texts
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["embeddings"]

def store_embeddings(texts, embeddings, metadata=None):
    documents = []
    for i, emb in enumerate(embeddings):
        doc = {
            "id": str(uuid.uuid4()),  # ID deve ser uma string
            "embedding": emb,  # Embedding deve ser uma lista
            "metadata": metadata[i] if metadata else {}  # Metadata deve ser um dicionário
        }
        documents.append(doc)

    # Verifique o formato dos documentos
    for doc in documents:
        if not isinstance(doc["id"], str):
            raise ValueError(f"Document ID should be a string, got {type(doc['id'])}.")
        if not isinstance(doc["embedding"], list):
            raise ValueError(f"Document embedding should be a list, got {type(doc['embedding'])}.")
        if not isinstance(doc["metadata"], dict):
            raise ValueError(f"Document metadata should be a dict, got {type(doc['metadata'])}.")

    try:
        collection.add(documents)
    except Exception as e:
        print(f"Failed to add documents: {e}")


def get_relevant_context(query_embedding, top_k=5):
    results = collection.query(query_embedding, top_k=top_k)
    return [res["metadata"] for res in results]

def add_message_to_context(message, metadata):
    embeddings = generate_embeddings([message])
    store_embeddings([message], embeddings, [metadata])
