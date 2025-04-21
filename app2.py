import streamlit as st
import requests

# Hugging Face API Token
HUGGINGFACE_API_TOKEN = "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"
MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

# Function to call Hugging Face API
def generate_response(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512,
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return ""

# --- Streamlit App ---
st.set_page_config(page_title="Chat with DeepSeek", page_icon="🤖", layout="centered")

st.title("🤖 DeepSeek Chat (Qwen-1.5B Style)")
st.markdown("A mini ChatGPT clone powered by `DeepSeek-R1-Distill-Qwen-1.5B`")

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role, content = msg["role"], msg["content"]
    if role == "user":
        st.chat_message("user").markdown(content)
    else:
        st.chat_message("assistant").markdown(content)

# Input box
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = generate_response(prompt)
            # Only include the assistant's new part of the message
            reply_cleaned = reply[len(prompt):].strip()
            st.markdown(reply_cleaned)
            st.session_state.messages.append({"role": "assistant", "content": reply_cleaned})
def build_message_history():
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
    ]

def generate_response():
    messages = build_message_history()

    payload = {
        "inputs": {
            "messages": messages
        },
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512,
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()["generated_text"]
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return ""
