from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurando o WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Acessa o WhatsApp Web
driver.get("https://web.whatsapp.com")

# Tempo para escanear o QR code
time.sleep(20)

def send_message_to_group(group_name, message):
    # Procurando o grupo pelo nome
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)
    
    time.sleep(2)
    
    # Seleciona o campo de mensagem
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    message_box.send_keys(message + Keys.ENTER)

# Função para monitorar mensagens e responder a comandos específicos
def check_for_new_messages(group_name):
    last_message_text = ""  # Variável para armazenar a última mensagem processada
    while True:
        try:
            # Seleciona o grupo para monitoramento
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.clear()
            search_box.send_keys(group_name + Keys.ENTER)
            time.sleep(2)
            
            # Encontra todas as mensagens recentes
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
            last_message = messages[-1].text  # Obtém a última mensagem
            
            # Verifica se a última mensagem é diferente da última processada
            if last_message != last_message_text:
                print(f"Última mensagem: {last_message}")
                last_message_text = last_message  # Atualiza a mensagem processada
                
                # Verifica se a última mensagem contém um comando específico
                if "!comando" in last_message:
                    send_message_to_group(group_name, "Resposta ao comando específico!")
                elif "!help" in last_message:
                    send_message_to_group(group_name, "Comandos disponíveis: !comando, !help")
                elif "!joao" in last_message:
                    send_message_to_group(group_name, "joao")
                
        except Exception as e:
            print(f"Erro: {str(e)}")
        time.sleep(5)

# Nome do grupo
group_name = "Pubzinho Season 7"

# Envia uma mensagem inicial para o grupo
send_message_to_group(group_name, "Bot ativado!")

# Monitora e responde às mensagens do grupo
check_for_new_messages(group_name)
