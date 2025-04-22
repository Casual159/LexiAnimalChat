# lexi_cli.py
import argparse
import subprocess
import requests
import json
import os

API_URL = "http://127.0.0.1:8000"  # agent
TOOLS_API = "http://127.0.0.1:8001"  # backend API

def run_app():
    subprocess.run(["python", "app.py"])

def run_check():
    subprocess.run(["python", "assistant_cli.py", "--check"])

def run_status():
    r = requests.get(f"{API_URL}/navigace")
    print("🧭 Agent říká:", r.json().get("navrh", "Nedostupné"))

def run_review():
    r = requests.get(f"{API_URL}/code-review")
    print("🧠 Code Review:", json.dumps(r.json(), indent=2, ensure_ascii=False))

def run_tests():
    result = subprocess.run(["pytest", "test_smoke.py", "-v"], capture_output=False)
    if result.returncode == 0:
        print("✅ Všechny testy proběhly úspěšně.")
    else:
        print("❌ Některé testy selhaly.")

def add_note(note):
    notes_file = "project_status.json"
    if os.path.exists(notes_file):
        with open(notes_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    notes = data.get("poznámky", [])
    notes.append(note)
    data["poznámky"] = notes

    with open(notes_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("📝 Poznámka přidána.")

# --- Hlavní orchestrátor projektu ---
parser = argparse.ArgumentParser()
parser.add_argument("prikaz", help="Zadej příkaz: run | status | check | review | deploy | note")
parser.add_argument("args", nargs="*", help="Volitelné argumenty (např. poznámka)")
args = parser.parse_args()

match args.prikaz:
    case "run":
        run_app()
    case "status":
        run_status()
    case "check":
        run_check()
    case "review":
        run_review()
    case "test":
        run_tests()
    case "note":
        add_note(" ".join(args.args))
    case "deploy":
        print("🚀 Příprava nasazení probíhá...")
    case _:
        print("❓ Neznámý příkaz")