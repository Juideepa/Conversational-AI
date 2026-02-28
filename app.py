import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ------------------ CONFIG ------------------ #

st.set_page_config(page_title="Voice AI Assistant", layout="centered")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ------------------ UI HEADER ------------------ #

st.title("🎤 AI Voice Assistant")
st.markdown("Powered by Gemini 2.5 Flash-Lite")
st.divider()

# ------------------ SESSION MEMORY ------------------ #

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ------------------ VOICE INPUT COMPONENT ------------------ #

voice_text = components.html("""
<div style="text-align:center;">
<button onclick="startRecognition()" 
style="padding:12px 24px; font-size:18px; background:linear-gradient(90deg,#00f5ff,#ff00c8); color:white; border:none; border-radius:12px; cursor:pointer;">
🎙️ Click to Speak
</button>
</div>

<script>
var recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';

recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: transcript,
    }, '*');
};

function startRecognition() {
    recognition.start();
}
</script>
""", height=120)

# ------------------ PROCESS VOICE ------------------ #

if voice_text:
    st.chat_message("user").write(voice_text)

    response = st.session_state.chat.send_message(voice_text)

    st.chat_message("assistant").write(response.text)

st.divider()
st.caption("⚡ Voice-enabled chatbot built with Streamlit + Gemini API")
