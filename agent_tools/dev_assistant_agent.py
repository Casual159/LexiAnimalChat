# dev_assistant_agent.py – pomocný agent pro vývojáře

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

### --- MODELY ---
class ProjektInfo(BaseModel):
    slozky: list[str]
    ma_env: bool = False
    ma_venv: bool = False
    obsahuje: list[str] = []

class DeployRequest(BaseModel):
    cil: str  # 'local' | 'hf_spaces' | 'railway'

class ToolRequest(BaseModel):
    nazev: str
    ucel: str
    vstupy: list[str]

### --- STAV PROJEKTU ---
projekt = {
    "slozky": [],
    "env": False,
    "venv": False,
    "soubory": [],
    "nasazeno": False
}

### --- ENDPOINTY ---
@app.post("/check_structure")
def check_structure(data: ProjektInfo):
    projekt["slozky"] = data.slozky
    projekt["env"] = data.ma_env
    projekt["venv"] = data.ma_venv
    projekt["soubory"] = data.obsahuje
    return {"stav": "načteno", "analyza": projekt}

@app.post("/deploy")
def deploy(data: DeployRequest):
    if data.cil == "local":
        return {"info": "Spusť pomocí: uvicorn tools_api:app --reload"}
    elif data.cil == "hf_spaces":
        return {"info": "Vytvoř Huggingface Space typu 'Gradio / FastAPI', nahraj soubory a nastav requirements.txt."}
    elif data.cil == "railway":
        return {"info": "Na railway.app vytvoř projekt, pushni repo a nastav port 8000."}
    else:
        return {"chyba": "Neznámý cíl nasazení."}

@app.post("/add_tool")
def add_tool(data: ToolRequest):
    funkce = {
        "name": data.nazev,
        "description": data.ucel,
        "parameters": {
            "type": "object",
            "properties": {k: {"type": "string"} for k in data.vstupy},
            "required": data.vstupy
        }
    }
    return {"tool_json": funkce, "navrh": f"Zaregistruj tento tool do agenta: {data.nazev}"}

@app.get("/navigace")
def navrh_dalsiho_kroku():
    if not projekt["env"]:
        return {"navrh": "Vytvoř .env soubor a nastav OPENAI_API_KEY a OPENAI_ASSISTANT_ID."}
    if "tools_api.py" not in projekt["soubory"]:
        return {"navrh": "Chybí backend API. Vytvoř nebo zkontroluj tools_api.py."}
    if not projekt["nasazeno"]:
        return {"navrh": "Zvaž nasazení API na Huggingface nebo Railway."}
    return {"navrh": "Vše vypadá dobře. Můžeš testovat agenta."}

@app.get("/code_review")
def code_review():
    if not projekt["soubory"]:
        return {"review": "Nejsou načtené žádné soubory. Spusť nejdříve --check."}
    
    podezrele = [s for s in projekt["soubory"] if "__" in s or "temp" in s or "copy" in s or "backup" in s]
    chybne_py = [s for s in projekt["soubory"] if s.endswith(".py") and s.startswith("test_") is False and "main" not in s and "app" not in s and "backend" not in s]
    test_soubory = [s for s in projekt["soubory"] if s.startswith("test_") or "/tests/" in s]

    return {
        "review": {
            "podezrele_soubory": podezrele,
            "chybi_testy": len(test_soubory) == 0,
            "navrh": "Zvaž přidání smoke testů a pojmenování testovacích souborů prefixem 'test_'."
        }
    }
