import os
import requests
import numpy as np
import faiss
from dotenv import load_dotenv

load_dotenv()
context_file_path = 'clean-code.txt'
faiss_index_path = 'faiss_index.index'

MAX_AMOUNT_MESSAGES = int(os.getenv("MAX_AMOUNT_MESSAGES", 10))
index = faiss.read_index(faiss_index_path)

message_history = []

def generate_embedding(text, model="llama3"):
    url = os.getenv("API_EMBEDDING_URL", "https://ollama.chargedcloud.com.br/api/embed")
    data = {
        "model": model,
        "input": [text]
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json().get("embeddings", [])[0]

def list_documents():
    if os.path.exists(context_file_path):
        with open(context_file_path, 'r') as file:
            return [line.strip() for line in file]
    else:
        return []

def get_relevant_context(query_text, top_k=5):
    query_embedding = generate_embedding(query_text)
    query_np = np.array([query_embedding]).astype('float32')
    
    distances, indices = index.search(query_np, k=top_k)
    all_texts = list_documents()
    results = [all_texts[i] for i in indices[0] if i < len(all_texts)]
    return " ".join(results)

def get_api_response(prompt, context=""):
    maximum_characters = int(os.getenv("CHARACTERS_AMOUNT", 100))

    system_instructions = (
        "Você é um assistente PT-BR especializado em Clean Code e boas práticas de programação. "
        "Na primeira interação, cumprimente o usuário de maneira educada. "
        "Responda estritamente no tema de Clean Code e boas práticas de programação; "
        "caso contrário, informe que não pode responder. "
        f"Sua resposta deve ser limitada a quantidade de caracteres: {maximum_characters}, e responda em PT-BR."
    )

    history = "\n".join([f"Usuário: {msg['user']}\nAssistente: {msg['assistant']}" for msg in message_history])
    full_prompt = f"{system_instructions}\n\n{history}\n\n{context}\n\nUsuário: {prompt}\nAssistente:" if context else f"{system_instructions}\n\n{history}\n\nUsuário: {prompt}\nAssistente:"

    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.1:latest",
        "prompt": full_prompt,
        "stream": False
    }
    url = os.getenv("API_COMPLETION_URL", "https://ollama.chargedcloud.com.br/api/generate")
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    
    assistant_response = response_data.get('response', "Resposta não encontrada")
    message_history.append({"user": prompt, "assistant": assistant_response})

    if len(message_history) > MAX_AMOUNT_MESSAGES:
        message_history.pop(0)

    return assistant_response

def main():
    print("Digite sua pergunta ou 'sair' para encerrar:")
    
    while True:
        user_input = input("Você: ")
        
        if user_input.lower() == 'sair':
            print("Encerrando...")
            break
        
        try:
            context = get_relevant_context(user_input)
            response = get_api_response(user_input, context)
            print("Resposta da API:", response)
        except Exception as e:
            print("Erro ao conectar com a API:", e)

if __name__ == "__main__":
    main()
