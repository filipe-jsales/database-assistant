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
from ..embeddings.embedding_manager import store_embeddings, generate_embeddings, list_documents, get_relevant_context, add_message_to_context

def my_function():
    global pegar_mensagem_random
    pegar_mensagem_random = True

def init(start_message, group_name, rvc, driver, engine, use_audio, response_prefix=""):
    global pegar_mensagem_random
    schedule.every(2).hours.do(my_function)
    schedule.run_pending()
    if len(response_prefix) > 0:
        response_prefix += " "
    send_message_to_group(driver, group_name, response_prefix + start_message)
    global message_history
    last_message_text = ""
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(group_name + Keys.ENTER)
    search_box.clear()
    while True:
        schedule.run_pending()
        try:
            messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
            last_message_element = messages[-1]
            last_message = extract_message_text(last_message_element)
            sender_name = extract_sender(last_message_element)

            if pegar_mensagem_random or (last_message != last_message_text and last_message.strip()):
                print(f"Última mensagem: {sender_name} - {last_message}")
                last_message_text = last_message

                if last_message.startswith("!duta") or pegar_mensagem_random:
                    pegar_mensagem_random = False
                    user_message = last_message.replace("!duta", "").strip()
                    member_name = get_member_name_from_message(user_message)
                    context = member_contexts.get(member_name, "")
                    previous_context = sender_name + ": " + user_message
                    print('previous context', previous_context)

                    if user_message:
                        full_prompt = ''
                        # TODO: append de todo o histórico de mensagems
                        for message in message_history:
                            full_prompt += " Leve em consideração que uma das mensagens anteriores foi: " + message
                        full_prompt += f"Pergunta: {context} {user_message}"
                        response = get_api_response(full_prompt)
                        print(response)
                        # TODO: melhorar histórico de mensagems
                        message_history.append(user_message)
                        if len(message_history) > 15:
                            message_history.pop(0)
                        message_history.append(response)
                        if len(message_history) > 15:
                            message_history.pop(0)
                        if use_audio:
                            choice = random.randint(1, 100)
                            print("random: " + str(choice))
                            if choice <= 20:
                                record_and_send_audio(rvc, driver, engine, group_name, response_prefix + response)
                            else:
                                send_message_to_group(driver, group_name, response_prefix + response)
                        else:
                            send_message_to_group(driver, group_name, response_prefix + response)
                    add_message_to_context(previous_context)
                    list_documents()
                    user_message_embedding = generate_embeddings([user_message])[0]
                    relevant_contexts = get_relevant_context(user_message_embedding)

                    full_prompt = '\n'.join(relevant_contexts) + f"\nMensagem do usuário: {context} {user_message}"
                    print('full prompt:', full_prompt)

                    response = get_api_response(full_prompt)
                    print(response)

                    add_message_to_context(user_message)
                    add_message_to_context(response)

                    if use_audio:
                        choice = random.randint(1, 100)
                        print("random: " + str(choice))
                        if choice <= 20:
                            record_and_send_audio(driver, engine, group_name, response)
                        else:
                            send_message_to_group(driver, group_name, response)
                    else:
                        send_message_to_group(driver, group_name, response)

                elif last_message.startswith("!everyone"):
                    send_mentions_one_by_one(driver, group_name)

                elif any(banned_word in last_message.lower() for banned_word in banned_words):
                    send_message_to_group(driver, group_name, "opa irmão, sem palavrão aí paizão, grupo da família aqui")

                elif any(bot_word in last_message.lower() for bot_word in bot_words):
                    prompt = "me diga que você não é um bot, de forma rude e usando palavrão em 1/5 das vezes"
                    response = get_api_response(prompt)
                    send_message_to_group(driver, group_name, response)

                elif last_message.startswith("!audio") and use_audio:
                    user_message = last_message.replace("!audio", "").strip()

                    member_name = get_member_name_from_message(user_message)
                    context = member_contexts.get(member_name, "")
                    if user_message:
                        full_prompt = ''
                        # TODO: append de todo o histórico de mensagems
                        for message in message_history:
                            full_prompt += " Leve em consideração que uma das mensagens anteriores foi: " + message
                        full_prompt += f"Pergunta: {context} {user_message}"
                        response = get_api_response(full_prompt)
                        print(response)
                        # TODO: melhorar histórico de mensagems
                        message_history.append(user_message)
                        if len(message_history) > 15:
                            message_history.pop(0)
                        message_history.append(response)
                        if len(message_history) > 15:
                            message_history.pop(0)
                        record_and_send_audio(rvc, driver, engine, group_name, response_prefix+response)

        except Exception as e:
            print(f"Erro: {str(e)}")
        time.sleep(5)