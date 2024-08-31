import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from context import member_contexts, banned_words, bot_words, pingar_todos


def send_message_to_group(driver, group_name, message):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(group_name + Keys.ENTER)

    time.sleep(2)

    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
    message_box.send_keys(message + Keys.ENTER)


def send_mentions_one_by_one(driver, group_name):
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

def extract_message_text(message_element):
    try:
        text_element = message_element.find_element(By.CSS_SELECTOR, 'span.selectable-text')
        return text_element.text
    except:
        return message_element.text

def extract_sender(message_element):
    try:
        text_element = message_element.find_element(By.CSS_SELECTOR, 'span[dir="auto"]')
        return get_member_name_from_message(text_element.text)
    except:
        return message_element.text

def get_member_name_from_message(message, group_members):
    for member in group_members:
        if member.lower() in message.lower():
            return member
    return None