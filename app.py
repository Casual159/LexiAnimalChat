import os
import sys
import gradio as gr
import soundfile as sf
import io
from tts_utils import generate_tts_audio
from stt_utils import transcribe_audio

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import wave
from chat_backend import (
    send_message,
    # extract_animal_topic, -- zřejmě není potřeba
    # get_animal_info, -- zřejmě není potřeba
    get_active_animal,  # 🔧 přidáno kvůli chybějícímu importu
    get_animal_data
)

def shutdown_app():
    print("Aplikace se ukončuje...")
    sys.exit()

def chat(user_input, history, current_img, current_desc):
    reply = send_message(user_input)
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": reply})

    audio_bytes = generate_tts_audio(reply)
    if audio_bytes:
        temp_path = "temp_response.mp3"
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)
        audio_output = gr.update(value=temp_path, visible=True)
    else:
        audio_output = gr.update(visible=False)

    zvire = get_active_animal(user_input)

    if not zvire:
        return "", history, gr.update(value=current_img, visible=bool(current_img)), gr.update(value=current_desc, visible=bool(current_desc)), current_img, current_desc, audio_output

    info = get_animal_data()

    audio_bytes = generate_tts_audio(reply)

    if audio_bytes:
        temp_path = "temp_response.mp3"
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)
        audio_output = gr.update(value=temp_path, visible=True)
    else:
        audio_output = gr.update(visible=False)

    if info:
        img = info["image"]
        desc = info["popis"]
        return "", history, gr.update(value=img, visible=True, label="Zvíře: " + zvire), gr.update(value="### " + zvire + "\n" + desc, visible=True), img, desc, audio_output
    else:
        return "", history, gr.update(visible=False), gr.update(visible=False), None, None, audio_output

def is_audio_too_long(audio_array, sample_rate, max_seconds=10):
    duration = len(audio_array) / float(sample_rate)
    return duration > max_seconds

def handle_audio(audio_data, history, current_img, current_desc):
    print(f"📂 Audio data ke kontrole: {audio_data}")
    if not audio_data:
        print("⚠️ Žádné audio data.")
        return "", history + [{"role": "user", "content": "(žádná audio data)"}], \
            gr.update(value=current_img, visible=bool(current_img)), \
            gr.update(value=current_desc, visible=bool(current_desc)), \
            current_img, current_desc, gr.update(visible=False)
    
    sample_rate, audio_array = audio_data

    if is_audio_too_long(audio_array, sample_rate):
        print("⚠️ Příliš dlouhé audio.")
        return "", history + [{"role": "user", "content": "(příliš dlouhá zpráva nebo chyba)"}], \
            gr.update(value=current_img, visible=bool(current_img)), \
            gr.update(value=current_desc, visible=bool(current_desc)), \
            current_img, current_desc, gr.update(visible=False)

    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, audio_array.reshape(-1, 1), sample_rate, format="WAV")
    audio_buffer.seek(0)
    user_input = transcribe_audio(audio_buffer)
    print(f"📝 Výstup transkripce: {user_input}")

    if not user_input or len(user_input.strip()) < 3:
        print("⚠️ Neplatný vstup nebo prázdný přepis")
        return "", history + [{"role": "user", "content": "(nerozpoznáno)"}], \
            gr.update(value=current_img, visible=bool(current_img)), \
            gr.update(value=current_desc, visible=bool(current_desc)), \
            current_img, current_desc, gr.update(visible=False)

    return chat(user_input, history, current_img, current_desc)

# --- UI layout ---
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=2):  # CHAT PANEL
            chatbot = gr.Chatbot(type="messages")
            msg = gr.Textbox(label="Zeptej se zvířecího kamaráda:")
            voice_input = gr.Audio(sources=["upload", "microphone"], type="numpy", label="Namluv nebo nahraj audio", interactive=True)
            clear = gr.Button("Vymazat konverzaci")
            shutdown = gr.Button("🛑 Vypnout aplikaci")

        with gr.Column(scale=1):  # INFO PANEL
            image = gr.Image(label="Zvíře, o kterém mluvíme", visible=False)
            description = gr.Markdown(visible=False)
            audio = gr.Audio(label="Odpověď", visible=False, interactive=False, type="filepath")

    # --- vnitřní stavy ---
    state = gr.State([])  # konverzace
    img_state = gr.State(value=None)  # poslední známý obrázek
    desc_state = gr.State(value=None)  # poslední známý popis

    # --- propojení logiky ---
    msg.submit(
        chat,
        [msg, state, img_state, desc_state],
        [msg, chatbot, image, description, img_state, desc_state, audio]
    )
    
    voice_input.change(
        handle_audio,
        [voice_input, state, img_state, desc_state],
        [msg, chatbot, image, description, img_state, desc_state, audio]
    )
    
    clear.click(lambda: [], None, chatbot)
    shutdown.click(fn=shutdown_app)

demo.queue().launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), auth=("admin", "tajneheslo"))