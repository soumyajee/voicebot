import openai
import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import tempfile
import requests
import os
import time
from dotenv import load_dotenv

# ✅ Load API Key from Environment Variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("⚠️ OpenAI API Key not found! Set it in a .env file or environment variable.")
    st.stop()

# ✅ Function to Record Audio
def record_audio(duration=5, sample_rate=44100):
    st.write("🎤 Recording... Speak now!")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    st.write("✅ Recording complete!")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file.name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    return temp_file.name

# ✅ Step 1: Transcribe Audio (Speech-to-Text)
def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    try:
        return response.text  # Extract transcribed text
    except Exception as e:
        st.error(f"⚠️ Error transcribing audio: {str(e)}")
        return None

# ✅ Step 2: Generate GPT-4o Response
def get_gpt4o_response(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                      {"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"⚠️ Error getting GPT-4o response: {str(e)}")
        return None

# ✅ Step 3: Convert GPT-4o Response to Speech
def text_to_speech(text):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {"Authorization": f"Bearer {openai.api_key}", "Content-Type": "application/json"}
    data = {"model": "tts-1", "input": text, "voice": "alloy"}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        audio_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        with open(audio_file_path, "wb") as f:
            f.write(response.content)
        return audio_file_path
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error generating speech: {str(e)}")
        return None

# ✅ Streamlit UI
st.title("🎙️ AI Voice Bot with GPT-4o Audio")

# ✅ Select Input Mode (Record or Upload)
mode = st.radio("Choose an option:", ["🎤 Record Audio", "📂 Upload Audio"])

if mode == "🎤 Record Audio":
    st.write("🎤 Click below to record your voice.")

    if st.button("🎤 Start Recording"):
        audio_path = record_audio()  # ✅ Step 1: Record
        text_query = transcribe_audio(audio_path)  # ✅ Step 2: Transcribe

        if text_query:
            st.write("🗣️ **You said:**", text_query)
            response_text = get_gpt4o_response(text_query)  # ✅ Step 3: Get GPT Response

            if response_text:
                st.write("🤖 **GPT-4o:**", response_text)
                response_audio_path = text_to_speech(response_text)  # ✅ Step 4: Convert to Speech
                
                if response_audio_path:
                    st.audio(response_audio_path, format="audio/mp3")  # ✅ Step 5: Play Response

elif mode == "📂 Upload Audio":
    uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "m4a"])

    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(uploaded_file.read())  # Save uploaded file

        text_query = transcribe_audio(temp_file.name)  # ✅ Step 2: Transcribe

        if text_query:
            st.write("🗣️ **You said:**", text_query)
            response_text = get_gpt4o_response(text_query)  # ✅ Step 3: Get GPT Response

            if response_text:
                st.write("🤖 **GPT-4o:**", response_text)
                response_audio_path = text_to_speech(response_text)  # ✅ Step 4: Convert to Speech
                
                if response_audio_path:
                    st.audio(response_audio_path, format="audio/mp3")  # ✅ Step 5: Play Response
