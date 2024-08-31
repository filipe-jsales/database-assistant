import time
import unicodedata

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def send_message_to_group(driver, group_name, message):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)

    time.sleep(2)

    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    message_box.send_keys(message + Keys.ENTER)


def send_mentions_one_by_one(driver, group_name, group_members):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)

    time.sleep(2)
    for member in group_members:
        normalized_string = unicodedata.normalize('NFD', member)
        # Filter out the combining characters (diacritical marks)
        string_without_accents = ''.join(
            char for char in normalized_string if unicodedata.category(char) != 'Mn'
        )
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.clear()
        message_box.send_keys('@' + string_without_accents + Keys.ENTER)
        message_box.send_keys(Keys.ENTER)
        time.sleep(1)

def extract_message_text(message_element):
    try:
        text_element = message_element.find_element(By.CSS_SELECTOR, 'span.selectable-text')
        return text_element.text
    except:
        return message_element.text

def extract_sender(message_element, group_members):
    try:
        text_element = message_element.find_element(By.CSS_SELECTOR, 'span[dir="auto"]')
        return get_member_name_from_message(text_element.text, group_members).split('\n')[0]
    except:
        return message_element.text

def get_member_name_from_message(message, group_members):
    for member in group_members:
        if member.lower() in message.lower():
            return member
    return None