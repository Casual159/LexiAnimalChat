import os
import requests

def generate_tts_audio(text):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # výchozí hlas

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.1,
            "similarity_boost": 0.4
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        return response.content  # ← vracíme byty
    else:
        print("⚠️ Chyba při generování TTS:", response.text)
        return None