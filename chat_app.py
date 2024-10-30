import streamlit as st
import requests

# Configurações de interface
st.title("Assistente de Banco de Dados")
st.write("Faça suas perguntas sobre Banco de Dados!")

# Histórico de chat
if "history" not in st.session_state:
    st.session_state["history"] = []

# Input do usuário
user_input = st.text_input("Você:", "")

if user_input:
    # Envia a mensagem ao backend Flask e exibe a resposta
    response = requests.post("http://localhost:5000/chat", json={"input": user_input}).json()
    assistant_response = response.get("response", "Erro ao conectar com a API.")

    # Adiciona ao histórico
    st.session_state["history"].append({"user": user_input, "assistant": assistant_response})

# Exibe o histórico
for chat in st.session_state["history"]:
    st.write(f"Você: {chat['user']}")
    st.write(f"Assistente: {chat['assistant']}")
