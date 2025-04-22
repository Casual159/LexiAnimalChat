# tools.py

# --- DATOVÉ ZDROJE ---
import json

# Data o zvířatech (z JSON – můžeš načítat i z externího souboru)
with open("zvirata.json", encoding="utf-8") as f:
    animal_data = json.load(f)

session_profile = {}

# --- FUNKCE AGENTA ---

def uloz_profil(jméno=None, věk=None, zvíře=None):
    if jméno:
        session_profile["jméno"] = jméno
    if věk:
        session_profile["věk"] = věk
    if zvíře:
        session_profile["zvíře"] = zvíře
    return {
        "status": "uloženo",
        "profil": session_profile
    }

def get_animal_info(zvíře):
    z = zvíře.lower()
    if z in animal_data:
        return {
            "popis": animal_data[z]["popis"],
            "image": animal_data[z]["image"]
        }
    else:
        return {
            "popis": "Tohle zvíře zatím nemám v katalogu.",
            "image": None
        }

def generate_quiz(zvíře):
    # můžeš tu udělat reálný generátor nebo jen demo
    return {
        "otazka": f"Víš, čím se {zvíře} živí?",
        "typ": "otevřená otázka"
    }