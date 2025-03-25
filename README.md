# voicebot
AI Voice Bot with GPT-4o

This is a voice-based AI assistant built using OpenAI's GPT-4o, Whisper (Speech-to-Text), and Text-to-Speech (TTS) models. The app is developed using Streamlit and allows users to record or upload an audio file to receive AI-generated responses.

🚀 Features

🎤 Record Audio and transcribe speech using OpenAI's Whisper model.

📂 Upload Audio files for transcription.

🤖 GPT-4o Response generation based on transcribed text.

🔊 Convert AI Response to Speech using OpenAI's TTS API.

🎧 Play AI-generated Response Audio within the Streamlit app.

🛠️ Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/your-repo/voicebot.git
cd voicebot

2️⃣ Create & Activate Virtual Environment

On Windows:

python -m venv voicebot
voicebot\Scripts\activate

On macOS/Linux:

python3 -m venv voicebot
source voicebot/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file in the project directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

5️⃣ Run the Streamlit App

streamlit run app.py

📜 Usage

Select "Record Audio" to record your voice or "Upload Audio" to use an existing file.

The app will transcribe your speech using Whisper.

GPT-4o will generate a response based on the transcribed text.

The response will be converted to speech and played back.


