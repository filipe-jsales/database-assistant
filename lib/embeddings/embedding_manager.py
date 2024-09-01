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

def clean_duplicates(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            lines = file.readlines()

    unique_lines = set()
    cleaned_lines = []

    for line in lines:
        if line.startswith(('!', 'k', 'K', '0', '1', '2')):
            continue

        if line not in unique_lines:
            cleaned_lines.append(line)
            unique_lines.add(line)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

    print(f"Cleanup completed. {len(lines) - len(cleaned_lines)} duplicates removed.")

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
    print('list documents')
    if os.path.exists(context_file_path):
        with open(context_file_path, 'r') as file:
            lines = file.readlines()
            print('lines:', lines)
        return [line.strip() for line in lines]
    else:
        return []

def store_embeddings(texts):
    clean_duplicates(context_file_path)
    embeddings = generate_embeddings(texts)

    ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
    
    if len(embeddings) != len(ids):
        raise ValueError(f"Number of embeddings {len(embeddings)} must match number of ids {len(ids)}")

    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)

    with open(context_file_path, 'a', encoding='utf-8') as file:
        for text in texts:
            file.write(text + '\n')

def get_relevant_context(query_embedding, top_k=10):
    query_np = np.array([query_embedding]).astype('float32')
    
    distances, indices = index.search(query_np, k=top_k)
    
    all_texts = list_documents()
    results = [all_texts[i] for i in indices[0] if i < len(all_texts)]
    print('relevant context:', results)
    return results

def add_message_to_context(message):
    embeddings = generate_embeddings([message])
    store_embeddings([message])
