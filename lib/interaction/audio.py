import random

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from pygame import mixer

load_dotenv()

def record_and_send_audio(rvc, driver, engine, group_name, response):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)
    time.sleep(2)
    search_box.send_keys(group_name + Keys.ENTER)
    record_button = driver.find_element(By.XPATH, '//span[@data-icon="ptt"]')

    retry_with_backoff(play, rvc, engine, response, record_button)

    send_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Enviar"]')
    send_button.click()

def play(rvc, engine, message, record_button):
    current_directory = os.getcwd()
    original_audio_path = current_directory + os.getenv("ORIGINAL_AUDIO_FILE_PATH")
    ai_audio_path = current_directory + os.getenv("AI_AUDIO_FILE_PATH")


    engine.save_to_file(message, original_audio_path)
    engine.runAndWait()

    models = rvc.list_models()
    rvc.load_model(random.choice(models))
    rvc.set_params(f0up_key=2, protect=0.5)
    rvc.infer_file(original_audio_path, ai_audio_path)

    record_button.click()
    time.sleep(1)

    mixer.music.load(ai_audio_path)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    rvc.unload_model()

def retry_with_backoff(func, *args):
    attempt = 1
    max_attempts = 5
    while attempt <= max_attempts:
        try:
            func(*args)
            return
        except Exception as e:
            error_message = str(e)
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt == max_attempts or not error_message.startswith("RuntimeError: The size of tensor a"):
                raise AssertionError(f"Max attempts reached: {e}")
            attempt += 1