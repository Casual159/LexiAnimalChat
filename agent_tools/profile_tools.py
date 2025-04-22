# agent_tools/profile_tools.py

import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

session_profile = {}

# --- OpenAI funkcionalita pro extrakci profilu ---

functions = [
    {
        "name": "uloz_profil",
        "description": "Získá jméno, věk a oblíbené zvíře od dítěte.",
        "parameters": {
            "type": "object",
            "properties": {
                "jméno": {"type": "string", "description": "Jméno dítěte"},
                "věk": {"type": "integer", "description": "Věk dítěte"},
                "zvíře": {"type": "string", "description": "Oblíbené zvíře"}
            },
            "required": []
        }
    },
    {
        "name": "uloz_zvire_tema",
        "description": "Určí zvíře, které je hlavním tématem věty nebo otázky dítěte.",
        "parameters": {
            "type": "object",
            "properties": {
                "zvíře": {
                    "type": "string",
                    "description": "Zvíře, o kterém dítě mluví (přesně dle katalogu Zoo Praha)"
                }
            },
            "required": ["zvíře"]
        }
    }
]

# --- Extrakce profilu ---
def extract_profile_via_gpt(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[{"role": "user", "content": user_input}],
            functions=functions,
            function_call={"name": "uloz_profil"}
        )
        arguments = response.choices[0].message.function_call.arguments
        data = json.loads(arguments)
        session_profile.update(data)
        print("🎯 GPT PROFIL:", session_profile)
    except Exception as e:
        print("⚠️ Nepodařilo se extrahovat profil:", e)

# --- Extrakce tématu zvířete ---
def extract_animal_topic(user_input):
    try:
        system_message = {
            "role": "system",
            "content": (
                "Jsi chytrý asistent pro děti. Máš za úkol detekovat, o jakém zvířeti dítě mluví, "
                "ale pouze tehdy, když dítě zmíní nové konkrétní zvíře. "
                "Pokud dítě navazuje na předchozí zvíře a žádné jiné nejmenuje, nic nevracej a nech zvíře nezměněné. "
                "Použij funkci pouze pokud je zřejmá změna tématu."
            )
        }

        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                system_message,
                {"role": "user", "content": user_input}
            ],
            functions=functions,
            function_call="auto"
        )

        choice = response.choices[0].message
        if choice.function_call:
            arguments = choice.function_call.arguments
            data = json.loads(arguments)
            zvire = data.get("zvíře")
            print("🦁 GPT ZVÍŘE:", zvire)
            return zvire

        print("📭 GPT nezvolilo žádné nové zvíře – ponecháme předchozí.")
        return None

    except Exception as e:
        print("⚠️ Chyba při extrakci zvířete:", e)
        return None
