import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_MODEL = os.getenv("API_MODEL")

def get_api_response(input):
    headers = {"Content-Type": "application/json"}

    with open('instructions.txt', 'r', encoding='utf-8') as file:
        instructions = file.read().strip()

    formatted_instructions = f"""
    <s>[INST] {instructions} [/INST]</s>
    [INST] {input}
           Contexto: Você faz parte de um grupo de whatsapp que contém joão, pedro, ulisses, leo, filipe, marina, lua
           Resposta:
    [/INST]
    """

    print('Formatted instructions and input:', formatted_instructions)

    data = {
        "model": API_MODEL,
        "messages": [
            {"role": "user", "content": formatted_instructions}
        ],
        "stream": False
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response_data = response.json()
    return response_data['message']['content']
