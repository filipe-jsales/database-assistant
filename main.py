import os
import requests
import numpy as np
import faiss
from dotenv import load_dotenv

# Configuração inicial e carga de variáveis de ambiente
load_dotenv()
context_file_path = 'clean-code.txt'
faiss_index_path = 'faiss_index.index'  # Caminho para o índice FAISS

# Carrega o índice FAISS salvo
index = faiss.read_index(faiss_index_path)

# Função para gerar embeddings usando a API externa
def generate_embedding(text, model="llama3"):
    url = os.getenv("API_EMBEDDING_URL", "https://ollama.chargedcloud.com.br/api/embed")
    data = {
        "model": model,
        "input": [text]
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json().get("embeddings", [])[0]

# Função para listar os documentos armazenados no arquivo de contexto
def list_documents():
    if os.path.exists(context_file_path):
        with open(context_file_path, 'r') as file:
            return [line.strip() for line in file]
    else:
        return []

# Função para buscar o contexto relevante usando FAISS
def get_relevant_context(query_text, top_k=5):
    query_embedding = generate_embedding(query_text)
    query_np = np.array([query_embedding]).astype('float32')
    
    distances, indices = index.search(query_np, k=top_k)
    all_texts = list_documents()
    results = [all_texts[i] for i in indices[0] if i < len(all_texts)]
    return " ".join(results)  # Combina os resultados em um único contexto

# Função para fazer a chamada à API com o contexto
def get_api_response(prompt, context=""):
    headers = {"Content-Type": "application/json"}
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    data = {
        "model": "llama3.1:latest",
        "prompt": full_prompt,
        "stream": False
    }
    
    response = requests.post("https://ollama.chargedcloud.com.br/api/generate", json=data, headers=headers)
    response_data = response.json()
    return response_data.get('response', "Resposta não encontrada")

# Função principal para perguntas e respostas com contexto FAISS
def main():
    print("Digite sua pergunta ou 'sair' para encerrar:")
    
    while True:
        user_input = input("Você: ")
        
        if user_input.lower() == 'sair':
            print("Encerrando...")
            break
        
        try:
            # Obtém o contexto relevante do índice FAISS
            context = get_relevant_context(user_input)
            response = get_api_response(user_input, context)
            print("Resposta da API:", response)
        except Exception as e:
            print("Erro ao conectar com a API:", e)

if __name__ == "__main__":
    main()
