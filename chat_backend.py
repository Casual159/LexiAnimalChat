# Refaktorizovaný chat_backend.py (verze C: řízené rozdělení a čistý orchestrátor)
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from dotenv import load_dotenv
from openai import OpenAI

from agent_tools.profile_tools import extract_profile_via_gpt, extract_animal_topic, session_profile
from agent_tools.animal_utils import get_animal_info

load_dotenv()
client = OpenAI()
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

# Vlákno pro GPT
thread = client.beta.threads.create()

# --- HLAVNÍ FUNKCE ---
def send_message(user_input):
    # 1. Aktualizuj profil dítěte
    extract_profile_via_gpt(user_input)

    # 2. Zeptej se GPT asistenta
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # 3. Počkej na odpověď
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    reply = messages.data[0].content[0].text.value
    return reply

# --- AKTUÁLNÍ TÉMA ZVÍŘETE ---
def get_active_animal(user_input):
    animal = extract_animal_topic(user_input)
    if animal:
        session_profile["zvire"] = animal
    return session_profile.get("zvire")

# --- INFORMACE O ZVÍŘETI ---
def get_animal_data():
    if "zvire" in session_profile:
        return get_animal_info(session_profile["zvire"])
    return None
