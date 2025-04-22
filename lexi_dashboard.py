import gradio as gr
import subprocess
import os
import sys

def check_status():
    result = subprocess.run(["python", "assistant_cli.py", "--status"], capture_output=True, text=True)
    return result.stdout.strip()

def run_tests():
    result = subprocess.run(["python", "test_smoke.py"], capture_output=True, text=True)
    return result.stdout.strip()

def run_deploy():
    result = subprocess.run(["python", "assistant_cli.py", "--deploy"], capture_output=True, text=True)
    return result.stdout.strip()

def run_code_review():
    result = subprocess.run(["python", "assistant_cli.py", "--code-review"], capture_output=True, text=True)
    return result.stdout.strip()

def open_docs():
    return "Dokumentace: https://github.com/Casual159/AILessons/blob/main/README.md"

def show_env():
    result = subprocess.run(["curl", "http://127.0.0.1:8001/env-check"], capture_output=True, text=True)
    return result.stdout.strip()

def run_git_sync():
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    return result.stdout.strip()

def get_token_usage():
    return "Token usage tracking zatím není aktivní."

def launch_app():
    subprocess.Popen([sys.executable, "app.py"])
    return "Aplikace spuštěna na http://127.0.0.1:7860"

with gr.Blocks(title="Lexi – Správa projektu") as dashboard:
    gr.Markdown("## 🧠 Lexi – Vývojový Dashboard")
    
    with gr.Row():
        status_btn = gr.Button("🧭 Zkontroluj stav projektu")
        test_btn = gr.Button("🧪 Spusť testy")
        run_btn = gr.Button("🚀 Spusť aplikaci")
        deploy_btn = gr.Button("📦 Deploy na Railway")
        review_btn = gr.Button("🔍 Code Review")
        doc_btn = gr.Button("📘 Otevři dokumentaci")
        env_btn = gr.Button("📜 Zobraz ENV")
        repo_btn = gr.Button("🔁 Git Sync")
        tokens_btn = gr.Button("🧮 Token Usage")
    
    output = gr.Textbox(label="Výstup", lines=15)

    status_btn.click(fn=check_status, outputs=output)
    test_btn.click(fn=run_tests, outputs=output)
    run_btn.click(fn=launch_app, outputs=output)
    deploy_btn.click(fn=run_deploy, outputs=output)
    review_btn.click(fn=run_code_review, outputs=output)
    doc_btn.click(fn=open_docs, outputs=output)
    env_btn.click(fn=show_env, outputs=output)
    repo_btn.click(fn=run_git_sync, outputs=output)
    tokens_btn.click(fn=get_token_usage, outputs=output)

if __name__ == "__main__":
    dashboard.launch(server_port=7890, show_error=True)
