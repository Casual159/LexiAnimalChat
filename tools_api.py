# tools_api.py

from fastapi import FastAPI
from pydantic import BaseModel
from chat_backend import send_message
from tools import session_profile, get_animal_info, generate_quiz
import os

app = FastAPI()

class UserInput(BaseModel):
    text: str

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/ask")
def ask(input: UserInput):
    odpoved = send_message(input.text)
    return {"odpoved": odpoved}

@app.get("/profil")
def profil():
    return session_profile

@app.get("/zvire")
def zvire():
    zvire_nazev = session_profile.get("zvíře")
    if not zvire_nazev:
        return {"error": "Zvíře není známo."}
    info = get_animal_info(zvire_nazev)
    return info if info else {"error": "Zvíře nebylo nalezeno."}

@app.get("/quiz")
def quiz():
    zvire_nazev = session_profile.get("zvíře")
    if not zvire_nazev:
        return {"error": "Zvíře není známé."}
    return generate_quiz(zvire_nazev)

@app.get("/env-check")
def env_check():
    api_key = os.getenv("OPENAI_API_KEY")
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
    return {
        "OPENAI_API_KEY": bool(api_key),
        "OPENAI_ASSISTANT_ID": bool(assistant_id)
    }
