import streamlit as st
import requests

# Hugging Face API token
HUGGINGFACE_API_TOKEN = "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"

# Model endpoint
MODEL_ID = "microsoft/phi-3.5-mini-instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}


def query_phi(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 256}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        st.error(f"Request failed: {response.status_code}, {response.text}")
        return None
    return response.json()[0]["generated_text"]


# Streamlit App
st.title("🤖 Chat with Phi-3.5 Mini (Microsoft)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        response = query_phi(user_input)
        if response:
            st.session_state.chat_history.append(("phi", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Phi-3.5:** {msg}")
