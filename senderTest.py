import requests
from flask import Flask, request, jsonify
import requests
import pygame
from io import BytesIO

ESP32_IP = "172.20.10.3"  # Replace with your ESP32 IP
url = f"http://{ESP32_IP}/instruments"


def generate_and_play_music(prompt, duration):
    API_KEY = "sk_f732d418f48b4571e382ad86205011d0df0ea69420333b25"

    url = "https://api.elevenlabs.io/v1/music/generate"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
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
        
def main():  
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            instruments = str(response.text)
            prompt = f"Make any sort of upbeat tune using only these instruments: {instruments}"
            print(prompt)
            generate_and_play_music(prompt, 10)
        else:
            print("Server returned:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Connection failed:", e)
    
    

if __name__ == "__main__":
    main()
