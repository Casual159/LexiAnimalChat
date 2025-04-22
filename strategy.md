

 # Projektová strategie – Lexi, kamarád zvířátek
 
 ## 🎯 Cíl
 Vytvořit chytrou, hravou aplikaci pro děti (4–10 let), která propojuje:
 - přirozenou interakci s AI
 - poznávání zvířat a přírody
 - plynulý zážitek s vizuálním obsahem
 
 ## ⚙️ 1. Automatizace vývoje & agentní přístup
 - Interní CLI agent (`assistant_cli.py`, `dev_assistant_agent.py`)
 - Pomáhá s kontrolou struktury, návrhem dalšího kroku, code review
 - Do budoucna:
   - Generování testů
   - Detekce chyb a jejich návrh oprav
   - Automatické plánování nasazení (např. HuggingFace)
 
 ## 🧠 2. Dynamická interakce s dětmi
 - GPT funguje jako adaptivní zvířecí kamarád
 - Prompt reaguje na věk dítěte (4–10 let)
 - Konverzace se přizpůsobuje znalostem, tématu, emoci
 - Detekce tématu/zvířete (function calling + paměť)
 - Možnost rozšíření o “stav dítěte” nebo zájem
 
 ## 🎨 3. Bohatší vizuální výstup
 - Obrázky z JSON (zvíře → popis + obrázek)
 - Přechodné efekty (Ken Burns, tilt.js, hover)
 - Možnost propojit s Giphy/Pexels API pro video/GIF
 - Backend dává frontend komponentě URL podle tématu
 
 ## 🚀 4. MVP & test
 - Lokální Gradio verze funguje
 - Cíl: nasadit na HuggingFace pro veřejné testování
 - Git je připravený, `.env` je skrytý
 - Projekt strukturován (modulární backend, CLI agent, `tools_api`)
 
 ## 📦 Budoucí možnosti
 - Text-to-speech
 - Progresivní UI (např. v Reactu)
 - Uložení průběhu (např. mini “dětský deník”)
 - Více vrstev agentní logiky (motivace, hra, vědomosti)