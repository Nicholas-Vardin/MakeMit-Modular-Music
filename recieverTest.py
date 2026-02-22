
from flask import Flask, request, jsonify
import requests
import pygame
from io import BytesIO

app = Flask(__name__)

def generate_and_play_music(prompt, duration):
    API_KEY = "sk_a43bfffb18c47ff3f27040dd188c5267c6fa5c67aa65d46d"

    url = "https://api.elevenlabs.io/v1/music/generate"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": "Upbeat electronic background music with light drums",
        "duration_seconds": 30
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    if response.status_code == 200:
        pygame.mixer.init()
        audio_stream = BytesIO(response.content)

        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    else:
        print("Error:", response.text)

@app.route("/api/message", methods=["POST"])
def receive_message():
    data = request.json
    x = data.get("prompt")
    duration = data.get("duration", 30)
    prompt = "Lovely music coming from a violin"
    print(data)
    generate_and_play_music(prompt, duration)

    return jsonify({"status": "music triggered"}), 200

if __name__ == "__main__":
    app.run(port=5000)