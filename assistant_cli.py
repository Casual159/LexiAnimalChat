# assistant_cli.py

import requests
import os
import argparse

API_URL = "http://127.0.0.1:8000"

parser = argparse.ArgumentParser(description="Komunikuj s pomocným agentem")
parser.add_argument("--status", action="store_true", help="Zobrazí návrh dalšího kroku")
parser.add_argument("--check", action="store_true", help="Pošle aktuální stav projektu do agenta")
parser.add_argument("--add-tool", nargs=3, metavar=("NAZEV", "UCEL", "VSTUPY"), help="Vygeneruj JSON funkce pro agenta")
args = parser.parse_args()

# --- Funkce ---
def detect_project_structure():
    slozky = next(os.walk("."))[1]
    vsechny_soubory = []
    ignorovat_slozky = {"venv", ".git", "__pycache__", ".mypy_cache"}
    povolene_pripony = {".py", ".json", ".env", ".txt", ".xlsx"}

    for root, dirs, files in os.walk("."):
        # Filtruj adresáře
        dirs[:] = [d for d in dirs if d not in ignorovat_slozky]
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in povolene_pripony or f.startswith(".env"):
                rel_path = os.path.relpath(os.path.join(root, f), ".")
                vsechny_soubory.append(rel_path)

    ma_env = any(f.endswith(".env") or f == ".env" for f in vsechny_soubory)
    ma_venv = "venv" in slozky or any(".venv" in s for s in slozky)

    return {
        "slozky": slozky,
        "ma_env": ma_env,
        "ma_venv": ma_venv,
        "obsahuje": vsechny_soubory
    }

# --- ZPRACOVÁNÍ ---
if args.status:
    r = requests.get(f"{API_URL}/navigace")
    print("🧭 Agent radí:", r.json()["navrh"])

elif args.check:
    data = detect_project_structure()
    r = requests.post(f"{API_URL}/check_structure", json=data)
    print("📁 Projekt analyzován:")
    print(r.json())

elif args.add_tool:
    nazev, ucel, vstupy = args.add_tool
    vstupy_list = [v.strip() for v in vstupy.split(",")]
    payload = {
        "nazev": nazev,
        "ucel": ucel,
        "vstupy": vstupy_list
    }
    r = requests.post(f"{API_URL}/add_tool", json=payload)
    print("🔧 Vygenerovaný tool JSON:")
    print(r.json())

else:
    parser.print_help()
