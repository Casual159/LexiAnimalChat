# 🦊 Projekt Lexi – kamarád zvířátek

**Poslední aktualizace:** *duben 2025*  
**Repozitář:** [GitHub – AILessons](https://github.com/Casual159/AILessons)

---

## 🎯 Cíl projektu

Vytvořit chytrou, hravou aplikaci pro děti (4–10 let), která propojuje:
- přirozenou interakci s AI (GPT jako zvířecí kamarád),
- poznávání zvířat a přírody,
- bohatý vizuální výstup s interaktivními prvky.

---

## 🧱 Struktura a moduly

- `chat_backend.py` – orchestrátor konverzace a rozhraní pro Gradio
- `agent_tools/profile_tools.py` – zpracování profilu dítěte (jméno, věk, zvíře)
- `agent_tools/animal_utils.py` – práce se zvířaty, jejich info, obrázky
- `tools.py`, `tools_api.py` – pomocné funkce, API pro agenty
- `app.py` – frontend aplikace
- `dev_assistant_agent.py` – sledování stavu projektu a návrhy změn
- `assistant_cli.py` – CLI rozhraní pro status, kontrolu, review

---

## 🧠 Funkčnost a chování

- Aplikace se ptá dítěte na jméno, věk a oblíbené zvíře
- GPT funguje jako přizpůsobivý kamarád – reaguje na věk, tón, emoce
- Detekce zvířete pomocí function calling a paměti
- Vizuální výstup (obrázky + popisy) se mění podle tématu
- Možnost alternativních otázek pro starší děti:
  - „Jaké zvíře tě naposledy zaujalo?“
  - „O kterém zvířeti bys dnes chtěl mluvit?“

---

## 🎨 Vizuální rozvoj

### Hotovo:
- Zobrazení obrázku detekovaného zvířete
- Obrázek zůstává i při navazující konverzaci
- integrace TTS a STT

### V plánu:
- integrovat Pexels zdroje

- Efekty:
  - Ken Burns (zoom + posun)
  - Parallax při pohybu myši
  - Tilt.js – 3D náklon
  - SVG overlay (vlnky apod.)
  - Videa/GIFy (Giphy, Pexels API)

---

### Implementováno:
- Interní CLI (`assistant_cli.py`) a vývojový agent (`dev_assistant_agent.py`)
- Validace `.env`, struktury složek, kontrola stavu
- Podpora příkazů: `--status`, `--check`, `--code-review`
- Popis zvířete vedle obrázku
- integrace TTS a STT skrze "nahraj/přehraj" možnosti v gradiu

### V plánu:
- Automatické generování testů
- Detekce chyb a návrh oprav
- Obsahový asistent (kuriozity, popisky)
- Scheduler/Planner funkcí
- Konverzační paměť
- Automatické plánování deploye

---

## 🚀 Deployment

- `.env` obsahuje API klíče (OpenAI, Assistant ID)
- Lokální běh: Gradio + Uvicorn
- Plánované varianty nasazení: Railway
- Projekt zatím **není nasazen**

---

## ✅ Roadmap / ToDo

- [ ] Vylepšit vizuální efekty (Ken Burns, hover, video)
- [ ] Nasadit veřejnou verzi (HF / Railway)
- [ ] Rozšířit funkce agentů (scheduler, dětský deník)