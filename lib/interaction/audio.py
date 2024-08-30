from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pygame import mixer

def record_and_send_audio(driver, engine, group_name, response):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)
    time.sleep(2)
    search_box.send_keys(group_name + Keys.ENTER)


    record_button = driver.find_element(By.XPATH, '//span[@data-icon="ptt"]')
    record_button.click()
    time.sleep(2)
    play(engine, response)

    send_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Enviar"]')
    send_button.click()


def play(engine, message):
    engine.save_to_file(message, "../../speech.wav")
    engine.runAndWait()

    mixer.music.load("../../speech.wav")
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(1)