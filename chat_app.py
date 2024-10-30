import streamlit as st
import requests

st.title("Assistente de Banco de Dados")
st.write("Faça suas perguntas sobre Banco de Dados!")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Você:", "")

if user_input:
    response = requests.post("https://c57f-2804-4df4-8000-6560-78fa-370e-1ecd-23cd.ngrok-free.app/chat", json={"input": user_input}).json()
    assistant_response = response.get("response", "Erro ao conectar com a API.")

    st.session_state["history"].append({"user": user_input, "assistant": assistant_response})

for chat in st.session_state["history"]:
    st.write(f"Você: {chat['user']}")
    st.write(f"Assistente: {chat['assistant']}")
