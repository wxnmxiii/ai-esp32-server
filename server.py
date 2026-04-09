from flask import Flask, request, send_file
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "AI Server Running"

@app.route("/talk", methods=["POST"])
def talk():
    audio = request.files["audio"]

    # STT
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )
    user_text = transcript.text

    # AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}]
    )
    ai_text = response.choices[0].message.content

    # TTS
    speech = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=ai_text
    )

    file_path = "response.mp3"
    speech.stream_to_file(file_path)

    return send_file(file_path, mimetype="audio/mpeg")
