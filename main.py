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
from context import member_contexts, banned_words, bot_words, group_members, pingar_todos

SESSION_FILE = "whatsapp_session.pkl"
API_URL = "https://ollama.chargedcloud.com.br/api/chat"
API_MODEL = "llama3"

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=./chrome-data")
chrome_options.add_argument("--remote-debugging-port=9222")

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

def extract_message_text(message_element):
    try:
        text_element = message_element.find_element(By.CSS_SELECTOR, 'span.selectable-text')
        return text_element.text
    except:
        return message_element.text

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
        message_box.send_keys(mention + Keys.ENTER)
        message_box.send_keys(Keys.ENTER)
        time.sleep(1)

def check_for_new_messages(group_name):
    global message_history
    last_message_text = ""  
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(group_name + Keys.ENTER)
    search_box.clear()
    while True:
        try:
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
            last_message_element = messages[-1]
            last_message = extract_message_text(last_message_element)
            
            if last_message != last_message_text and last_message.strip():
                print(f"Última mensagem: {last_message}")
                last_message_text = last_message 

                message_history.append(last_message)
                if len(message_history) > 15:
                    message_history.pop(0)
                
                if last_message.startswith("!duta"):
                    user_message = last_message.replace("!duta", "").strip()

                    member_name = get_member_name_from_message(user_message)
                    context = member_contexts.get(member_name, "")
                    
                    if user_message:
                        full_prompt = f"{context} {user_message}"
                        response = get_api_response(full_prompt)
                        send_message_to_group(group_name, response)
                
                elif last_message.startswith("!everyone"):
                    send_mentions_one_by_one(group_name)
                
                elif any(banned_word in last_message.lower() for banned_word in banned_words):
                    send_message_to_group(group_name, "opa irmão, sem palavrão aí paizão, grupo da família aqui")
                    
                elif any(bot_word in last_message.lower() for bot_word in bot_words):
                    prompt = "me diga que você não é um bot, de forma rude e usando palavrão em 1/5 das vezes"
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
send_message_to_group(group_name, "oiiii primos")

check_for_new_messages(group_name)
