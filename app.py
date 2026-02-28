import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ------------------ SETUP ------------------ #

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.set_page_config(page_title="Voice AI Agent", layout="centered")
st.title("🎤 Browser Voice AI Assistant")

# Session Memory
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ------------------ JS Voice Input ------------------ #

voice_text = st.text_input("Voice Input", key="voice_input")

st.markdown("""
<script>
const recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.lang = "en-US";

function startRecognition() {
    recognition.start();
}

recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    const inputBox = window.parent.document.querySelector('input[data-testid="stTextInput"]');
    inputBox.value = transcript;
    inputBox.dispatchEvent(new Event('input', { bubbles: true }));
};
</script>

<button onclick="startRecognition()">🎙️ Speak</button>
""", unsafe_allow_html=True)

# ------------------ PROCESS INPUT ------------------ #

if voice_text:
    st.chat_message("user").write(voice_text)

    response = st.session_state.chat.send_message(voice_text)

    st.chat_message("assistant").write(response.text)
