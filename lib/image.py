import time

import requests
import base64
import os
from selenium.webdriver.common.by import By

current_directory = os.getcwd()
image_path = current_directory + os.getenv("IMAGE_FILE_PATH")

def create_fryed_stamp(driver, image_element):
    image_url = image_element.get_attribute("src")
    print(f"Image URL: {image_url}")

    if "," in image_url:
        base64_string = image_url.split(",")[1]
        image_data = base64.b64decode(base64_string)

        with open(image_path, "wb") as handler:
            handler.write(image_data)
    else:
        image_data = requests.get(image_url).content

        with open(image_path, "wb") as handler:
            handler.write(image_data)

    output_stamp(driver)

def output_stamp(driver):
    append_button = driver.find_element(By.XPATH, '//span[@data-icon="plus"]')
    append_button.click()

    input_element = driver.find_element(By.XPATH, '//span[text()="Nova figurinha"]/following::input[@type="file"]')
    input_element.send_keys(image_path)

    time.sleep(2)

    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    send_button.click()