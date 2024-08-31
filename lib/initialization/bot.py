import random
import time
import schedule

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lib.ai import get_api_response
from lib.interaction.audio import record_and_send_audio
from context import member_contexts, banned_words, bot_words, pingar_todos
from lib.interaction.message import extract_message_text, extract_sender, get_member_name_from_message, \
    send_message_to_group, send_mentions_one_by_one

message_history = []
pegar_mensagem_random = False
from lib.embeddings.embedding_manager import generate_embeddings, list_documents, get_relevant_context, add_message_to_context

def init(start_message, group_name, rvc, driver, engine, use_audio, response_prefix=""):
    global pegar_mensagem_random
    global message_history
    schedule.every(2).hours.do(set_read_recent_message)
    schedule.run_pending()
    if len(response_prefix) > 0:
        response_prefix += " "

    send_message_to_group(driver, group_name, response_prefix + start_message)
    focus_on_group(driver, group_name)

    group_members = get_member_list(driver)
    last_message_text = ""

    while True:
        schedule.run_pending()
        try:
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
            last_message_element = messages[-1]
            last_message = extract_message_text(last_message_element)
            sender_name = get_sender(messages, last_message_element, group_members)

            if pegar_mensagem_random or (last_message != last_message_text and last_message.strip()):
                print(f"Última mensagem: {sender_name} - {last_message}")
                last_message_text = last_message

                if last_message.startswith("!duta") or pegar_mensagem_random:
                    handle_duta_command(driver, engine, group_members, group_name, last_message, response_prefix, rvc,
                                        sender_name, use_audio)

                elif last_message.startswith("!bora"):
                    send_mentions_one_by_one(driver, group_name, group_members)

                elif any(banned_word in last_message.lower() for banned_word in banned_words):
                    send_message_to_group(driver, group_name, "opa irmão, sem palavrão aí paizão, grupo da família aqui")

                elif any(bot_word in last_message.lower() for bot_word in bot_words):
                    prompt = "me diga que você não é um bot, de forma rude e usando palavrão em 1/5 das vezes"
                    response = get_api_response(prompt)
                    send_message_to_group(driver, group_name, response)

                elif last_message.startswith("!audio") and use_audio:
                    handle_audio_command(driver, engine, group_members, group_name, last_message, response_prefix, rvc,
                                         sender_name)

        except Exception as e:
            print(f"Erro: {str(e)}")
        time.sleep(5)


def handle_audio_command(driver, engine, group_members, group_name, last_message, response_prefix, rvc, sender_name):
    user_message = last_message.replace("!audio", "").strip()
    member_name = get_member_name_from_message(user_message, group_members)
    context = member_contexts.get(member_name, "")
    previous_context = sender_name + ": " + user_message
    print('previous context', previous_context)

    add_message_to_context(previous_context)
    list_documents()
    # user_message_embedding = generate_embeddings([user_message])[0]
    # relevant_contexts = get_relevant_context(user_message_embedding)

    full_prompt = f"\nMensagem do usuário: {context} {user_message}"

    response = get_api_response(full_prompt)
    print('response full prompt:', response)

    add_message_to_context(response)
    if user_message:
        record_and_send_audio(rvc, driver, engine, group_name, response_prefix + response)


def handle_duta_command(driver, engine, group_members, group_name, last_message, response_prefix, rvc, sender_name,
                        use_audio):
    global pegar_mensagem_random
    pegar_mensagem_random = False
    user_message = last_message.replace("!duta", "").strip()
    member_name = get_member_name_from_message(user_message, group_members)
    context = member_contexts.get(member_name, "")
    previous_context = sender_name + ": " + user_message
    print('previous context', previous_context)

    add_message_to_context(previous_context)
    list_documents()
    # user_message_embedding = generate_embeddings([user_message])[0]
    # relevant_contexts = get_relevant_context(user_message_embedding)

    full_prompt = f"\nMensagem do usuário: {context} {user_message}"

    response = get_api_response(full_prompt)
    print('response full prompt:', response)

    add_message_to_context(response)
    if user_message:
        if use_audio:
            choice = random.randint(1, 100)
            print("random: " + str(choice))
            if choice <= 20:
                record_and_send_audio(rvc, driver, engine, group_name, response_prefix + response)
            else:
                send_message_to_group(driver, group_name, response_prefix + response)
        else:
            send_message_to_group(driver, group_name, response_prefix + response)


def set_read_recent_message():
    global pegar_mensagem_random
    pegar_mensagem_random = True

def get_member_list(driver):
    element = driver.find_element(By.XPATH, "//div[@id='main']//header//div[@role='button']")
    element.click()
    members_div = driver.find_element(By.XPATH, "//div[@aria-label[contains(., 'Lista de membros')]]")
    span_elements = members_div.find_elements(By.XPATH, ".//div[@role='gridcell']//span[@title]")
    group_members = [span.get_attribute("title") for span in span_elements]
    group_members.remove('Você')
    exit_button = driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='Fechar']")
    exit_button.click()
    return group_members

def focus_on_group(driver, group_name):
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(group_name + Keys.ENTER)
    search_box.clear()

def get_sender(messages, last_message_element, group_members):
    sender_name = extract_sender(last_message_element, group_members)
    deduct = 2
    while sender_name is None:
        next_message_index = len(messages) - deduct
        deduct += 1
        sender_name = extract_sender(messages[next_message_index], group_members)
    return sender_name