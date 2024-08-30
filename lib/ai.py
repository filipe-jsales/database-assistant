import requests

API_URL = "https://ollama.chargedcloud.com.br/api/chat"
API_MODEL = "llama3"

def get_api_response(prompt):
    headers = {"Content-Type": "application/json"}

    with open('instructions.txt', 'r', encoding='utf-8') as file:
        instructions = file.read()

    messages = [
        {"role": "user", "content": instructions + prompt}
    ]

    data = {
        "model": API_MODEL,
        "messages": messages,
        "stream": False
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response_data = response.json()
    return response_data['message']['content']