import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Hugging Face API config
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
API_TOKEN = "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"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to send prompt to HF and get image
def generate_image(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="SD 3.5 Image Generator", page_icon="🖼️")
st.title("🖼️ Text to Image Generator with Stable Diffusion 3.5")
st.markdown("Generate images using `stabilityai/stable-diffusion-3.5-large` via Hugging Face")

# Prompt input
prompt = st.text_input("Enter your prompt here")

if st.button("Generate Image") and prompt:
    with st.spinner("Generating image..."):
        image = generate_image(prompt)
        if image:
            st.image(image, caption="Generated Image", use_column_width=True)
