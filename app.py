import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3

# ------------------ SETUP ------------------ #

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ------------------ VOICE FUNCTIONS ------------------ #

def speak(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except:
            return "Sorry, I could not understand."

# ------------------ PAGE CONFIG ------------------ #

st.set_page_config(page_title="Voice AI Agent", layout="centered")

# ------------------ CUSTOM CSS ------------------ #

st.markdown("""
<style>
body {
    background: linear-gradient(to right, #141E30, #243B55);
    color: white;
}
.big-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #00f5ff;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #bbbbbb;
}
.stButton>button {
    background: linear-gradient(90deg, #00f5ff, #ff00c8);
    color: white;
    font-size: 18px;
    border-radius: 12px;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HERO IMAGE ------------------ #

st.image("voice_banner.jpg", use_container_width=True)

st.markdown('<div class="big-title">🎤 AI Voice Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Gemini 2.5 Flash-Lite</div>', unsafe_allow_html=True)

st.divider()

# ------------------ SESSION MEMORY ------------------ #

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ------------------ VOICE BUTTON ------------------ #

if st.button("🎙️ Start Speaking"):

    user_input = listen()

    st.chat_message("user").write(user_input)

    response = st.session_state.chat.send_message(user_input)

    st.chat_message("assistant").write(response.text)

    speak(response.text)

st.divider()
st.caption("⚡ Built using Streamlit + Gemini LLM | Session-based conversational memory")
