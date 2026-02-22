

import requests
import pygame
from io import BytesIO

API_KEY = "sk_f732d418f48b4571e382ad86205011d0df0ea69420333b25"

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