from dotenv import load_dotenv
import os
import openai

load_dotenv()

def transcribe_audio(audio_buffer):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        # Hack: přidej jméno jako kdyby to byl soubor
        audio_buffer.name = "temp.wav"
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_buffer,
            language="cs"
        )
        return transcript.text
    except Exception as e:
        print(f"⚠️ Chyba při transkripci audia: {e}")
        return None