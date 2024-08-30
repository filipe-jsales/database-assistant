import os
import requests
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import uuid

load_dotenv()

# client = chromadb.peClient()

client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "message_embeddings"
collection = client.get_or_create_collection(collection_name)
def generate_embeddings(texts, model="llama3"):
    url = os.getenv("API_EMBEDDING_URL", "https://ollama.chargedcloud.com.br/api/embed")
    data = {
        "model": model,
        "input": texts,
        "num_ctx": os.getenv("NUM_CTX", "4096"),
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json().get("embeddings", [])

def list_documents(collection_name="message_embeddings"):
    documents = collection.get()
    
    return documents

def store_embeddings(texts, collection_name="message_embeddings"):
    collection = client.get_or_create_collection(name=collection_name)
    embeddings = generate_embeddings(texts)

    print(f"Generated {len(embeddings)} embeddings.")
    print('texts', texts)
    
    ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
    print(ids)
    
    if len(embeddings) != len(ids):
        raise ValueError(f"Number of embeddings {len(embeddings)} must match number of ids {len(ids)}")

    collection.add(documents=texts, embeddings=embeddings, ids=ids)

    print(f"Inserted {len(texts)} embeddings into collection '{collection_name}'.")


# def query_context(query_texts, collection_name="message_embeddings", n_results=2):
#     results = collection.query(
#         query_texts=query_texts,
#         n_results=n_results
#     )
#     print('query', query_texts)
#     return results


def get_relevant_context(query_embedding, top_k=5):
    results = collection.query(query_embedding, top_k=top_k)
    return [res["metadata"] for res in results]

def add_message_to_context(message, metadata):
    embeddings = generate_embeddings([message])
    store_embeddings([message], embeddings, [metadata])
