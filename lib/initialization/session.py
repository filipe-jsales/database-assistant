import os
import pickle
import time
from dotenv import load_dotenv

load_dotenv()

SESSION_FILE = os.getenv("SESSION_FILE", "whatsapp_session.pkl")

def init(driver):
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "rb") as session_file:
            cookies = pickle.load(session_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    else:
        if "https://web.whatsapp.com" in driver.current_url:
            print("Por favor, escaneie o QR code para login no WhatsApp Web.")
            time.sleep(20)
            save_session(driver)
    time.sleep(5)

def save_session(driver):
    with open(SESSION_FILE, "wb") as session_file:
        pickle.dump(driver.get_cookies(), session_file)
