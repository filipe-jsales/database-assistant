from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pickle
import requests

SESSION_FILE = "whatsapp_session.pkl"
API_URL = "https://ollama.chargedcloud.com.br/api/chat"
API_MODEL = "llama3"

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=./chrome-data")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def load_session(driver):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "rb") as session_file:
            cookies = pickle.load(session_file)
            for cookie in cookies:
                driver.add_cookie(cookie)

def save_session(driver):
    with open(SESSION_FILE, "wb") as session_file:
        pickle.dump(driver.get_cookies(), session_file)

driver.get("https://web.whatsapp.com")

load_session(driver)
time.sleep(15)

if "https://web.whatsapp.com" in driver.current_url:
    print("Por favor, escaneie o QR code para login no WhatsApp Web.")
    time.sleep(5)
    save_session(driver)

def send_message_to_group(group_name, message):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)
    
    time.sleep(2)
    
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    message_box.send_keys(message + Keys.ENTER)

def get_api_response(prompt):
    headers = {"Content-Type": "application/json"}
    
    # Instruções claras sobre como o modelo deve responder
    instructions = (
        "Você é um jovem informal e direto. use as vezes 40 porcento das vezes a gíria 'mano' e seja "
        "informal, sem utilizar 'você', use 'tu'. Textos sempre no minúsculo e "
        "sem pontuações ou acentuações como exclamação, vírgula ou ponto final. "
        "você é assume a personalidade de um homem machista, homofóbico e racista. "
        "Responda com no máximo 40 caracteres. Se receber uma pergunta, tenha 20% "
        "de chance de responder de forma negativa ou dizendo que não sabe, de forma "
        "direta e com poucas palavras, por exemplo: 'sei não cara', 'sei n mano'. "
        "Pergunta: "
    )
    
    # Cria a mensagem com instrução e o prompt
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

def extract_message_text(message_element):
    try:
        text_element = message_element.find_element(By.CSS_SELECTOR, 'span.selectable-text')
        return text_element.text
    except:
        return message_element.text

banned_words = ["crl", "caralho", "porra", "vsf", "filha da puta", "fdp"]

bot_words = ["bot"]

group_members = ["pedro", "marina", "joao", "joão", "marcelo", "leo", "ulisses"]

pingar_todos = ["@pedro", "@star", "@jo", "@leo", "@ulisses"]

def get_member_name_from_message(message):
    for member in group_members:
        if member.lower() in message.lower():
            return member
    return None

message_history = []

def send_mentions_one_by_one(group_name):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)
    
    time.sleep(2)
    
    for mention in pingar_todos:
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.clear()
        message_box.send_keys(mention + Keys.ENTER)  # Envia a menção
        message_box.send_keys(Keys.ENTER)  # Pressiona Enter uma segunda vez para garantir o envio
        time.sleep(1)  # Adiciona um pequeno atraso entre as menções para evitar sobrecarregar a interface



def check_for_new_messages(group_name):
    global message_history
    last_message_text = ""  
    while True:
        try:
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(group_name + Keys.ENTER)
            time.sleep(2)
            
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
            last_message_element = messages[-1]
            last_message = extract_message_text(last_message_element)
            
            if last_message != last_message_text and last_message.strip():
                print(f"Última mensagem: {last_message}")
                last_message_text = last_message 

                # Adiciona a última mensagem ao histórico
                message_history.append(last_message)
                if len(message_history) > 10:
                    message_history.pop(0)  # Mantém um histórico de 10 mensagens
                
                # Ajuste o comportamento com base no histórico
                if last_message.startswith("!duta"):
                    user_message = last_message.replace("!duta", "").strip()
                    if user_message:
                        response = get_api_response(user_message)
                        send_message_to_group(group_name, response)
                
                elif last_message.startswith("!everyone"):
                    send_mentions_one_by_one(group_name)
                
                elif any(banned_word in last_message.lower() for banned_word in banned_words):
                    send_message_to_group(group_name, "opa irmão, sem palavrão aí paizão, grupo da família aqui")
                    
                elif any(bot_word in last_message.lower() for bot_word in bot_words):
                    prompt = "me diga que você não é um bot, de forma rude e podendo usar palavrão"
                    response = get_api_response(prompt)
                    send_message_to_group(group_name, response)
                    
        except Exception as e:
            print(f"Erro: {str(e)}")
        time.sleep(5)


def record_and_send_audio(group_name):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)
    time.sleep(2)
    search_box.send_keys(group_name + Keys.ENTER)


    record_button = driver.find_element(By.XPATH, '//span[@data-icon="ptt"]')
    record_button.click()
    
    time.sleep(5)

    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    send_button.click()

group_name = "Pubzinho Season 7"
send_message_to_group(group_name, "fala")

check_for_new_messages(group_name)
