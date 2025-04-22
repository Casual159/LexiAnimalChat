# agent_tools/animal_utils.py

import json

# --- Načtení dat ze zvirata.json ---
with open("zvirata.json", encoding="utf-8") as f:
    animal_data = json.load(f)

# --- Vrátí dict s popisem a obrázkem ---
def get_animal_info(zvire_nazev):
    """
    Vrátí dict s klíči 'image' a 'popis' pro dané zvíře.
    Pokud nenajde přesně, zkusí částečné shody.
    """
    if not zvire_nazev:
        return None

    zvire_nazev = zvire_nazev.lower()

    # 1. Přesná shoda
    if zvire_nazev in animal_data:
        return animal_data[zvire_nazev]

    # 2. Částečná shoda (např. "slon" → "slon africký")
    for klic in animal_data.keys():
        if zvire_nazev in klic:
            return animal_data[klic]

    return None

# --- Vrátí jen URL obrázku ---
def get_animal_image(zvire_nazev):
    info = get_animal_info(zvire_nazev)
    return info["image"] if info else None
