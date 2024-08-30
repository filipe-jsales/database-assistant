from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

load_dotenv()

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={os.getenv('CHROME_USER_DATA_DIR', './chrome-data')}")
chrome_options.add_argument(f"--remote-debugging-port={os.getenv('CHROME_REMOTE_DEBUGGING_PORT', '9222')}")

def init():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(os.getenv("WHATSAPP_WEB_URL", "https://web.whatsapp.com"))
    return driver
