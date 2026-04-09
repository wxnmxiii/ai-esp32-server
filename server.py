from flask import Flask, request, send_file
import openai
import os

app = Flask(__name__)

# ใส่ API KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "AI Server Running"

@app.route("/talk", methods=["POST"])
def talk():
    audio = request.files["audio"]

    # 1. Speech to Text
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )
    user_text = transcript.text
    print("User:", user_text)

    # 2. AI
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "คุณคือผู้ช่วยพูดจาสุภาพ สั้น เข้าใจง่าย"},
            {"role": "user", "content": user_text}
        ]
    )
    ai_text = response.choices[0].message.content
    print("AI:", ai_text)

    # 3. Text to Speech
    speech = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=ai_text
    )

    file_path = "response.mp3"
    speech.stream_to_file(file_path)

    return send_file(file_path, mimetype="audio/mpeg")