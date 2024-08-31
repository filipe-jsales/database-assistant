import os
import requests
import faiss
import numpy as np
import uuid
from dotenv import load_dotenv

load_dotenv()

embedding_dimension = 4096 
index = faiss.IndexFlatL2(embedding_dimension)

context_file_path = 'context.txt'

def generate_embeddings(texts, model="llama3"):
    url = os.getenv("API_EMBEDDING_URL", "https://ollama.chargedcloud.com.br/api/embed")
    data = {
        "model": model,
        "input": texts,
        "num_ctx": os.getenv("NUM_CTX", "4096"),
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    print('response for generate embeddings:', response)
    return response.json().get("embeddings", [])

def list_documents():
    if os.path.exists(context_file_path):
        with open(context_file_path, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    else:
        return []

def store_embeddings(texts):
    embeddings = generate_embeddings(texts)

    print(f"Generated {len(embeddings)} embeddings.")
    print('texts:', texts)
    
    ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
    print('ids:', ids)
    
    if len(embeddings) != len(ids):
        raise ValueError(f"Number of embeddings {len(embeddings)} must match number of ids {len(ids)}")

    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)

    with open(context_file_path, 'a') as file:
        for text in texts:
            file.write(text + '\n')

    print(f"Inserted {len(texts)} embeddings into FAISS index.")

def get_relevant_context(query_embedding, top_k=5):
    query_np = np.array([query_embedding]).astype('float32')
    
    distances, indices = index.search(query_np, k=top_k)
    
    all_texts = list_documents()
    results = [all_texts[i] for i in indices[0] if i < len(all_texts)]
    return results

def add_message_to_context(message):
    embeddings = generate_embeddings([message])
    store_embeddings([message])
