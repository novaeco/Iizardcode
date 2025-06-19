import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import threading, os, datetime, json

from hardware import send_serial_command

PROFILES_FILE = "profiles.json"
HIST_FILE = "historique_ia.json"
OPENAPI_FILE = "openapi.json"

def run_app():
    app = tb.Window(themename="darkly")
    app.title("DevCenter PRO (Modern & Hardware Ready)")
    app.geometry("1200x900")
    app.resizable(True, True)

    # ----- LOGS -----
    log_frame = tb.LabelFrame(app, text="🪵 Logs en direct", bootstyle="info")
    log_frame.pack(fill="both", expand=False, padx=10, pady=5)
    log_box = scrolledtext.ScrolledText(log_frame, height=8, font=("Consolas", 9), state="disabled")
    log_box.pack(fill="both", expand=True)
    def add_log(msg):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        log_box.config(state="normal")
        log_box.insert("end", f"[{now}] {msg}\n")
        log_box.config(state="disabled")
        log_box.see("end")

    # ----- TABS -----
    main_frame = tb.Notebook(app)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)
    tab_project = tb.Frame(main_frame)
    tab_ia = tb.Frame(main_frame)
    tab_git = tb.Frame(main_frame)
    tab_tools = tb.Frame(main_frame)
    main_frame.add(tab_project, text="📦 Projet")
    main_frame.add(tab_ia, text="🤖 Assistant IA")
    main_frame.add(tab_git, text="📤 GitHub")
    main_frame.add(tab_tools, text="🛠️ Outils avancés")

    # ---------- Fonctions Projet ----------
    def detect_com():
        try:
            import serial.tools.list_ports
            ports = list(serial.tools.list_ports.comports())
            if not ports:
                add_log("[ERR] Aucun port COM détecté")
                messagebox.showwarning("ESP32", "Aucun port COM détecté !")
                return None
            add_log(f"[OK] Port détecté : {ports[0].device}")
            return ports[0].device
        except Exception as e:
            add_log(f"[ERR] pyserial absent ou erreur : {e}")
            messagebox.showwarning("ESP32", "pyserial n'est pas installé !")
            return None

    def flash_esp32():
        port = detect_com()
        if not port:
            return
        # Exemple : simule un flash, à adapter avec ta commande
        add_log(f"[FLASH] (Fake) Flash ESP32 sur {port}")
        messagebox.showinfo("Flash ESP32", f"Flash simulé sur : {port}")

    def generate_project():
        os.makedirs("src", exist_ok=True)
        with open("src/main.c", "w") as f:
            f.write("// Entry point du projet généré\nint main() { return 0; }\n")
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# Projet ESP32/BPI généré par DevCenter\n")
        add_log("[OK] Projet ESP32/BPI généré.")

    def generate_workspace():
        ws = {"folders": [{"path": "."}], "settings": {}}
        with open(".code-workspace", "w", encoding="utf-8") as f:
            json.dump(ws, f, indent=2)
        add_log("[OK] .code-workspace généré.")

    def generate_openapi():
        openapi = {
            "openapi": "3.0.0",
            "info": {"title": "DevCenter API", "version": "1.0.0"},
            "paths": {}
        }
        with open(OPENAPI_FILE, "w", encoding="utf-8") as f:
            json.dump(openapi, f, indent=2)
        add_log("[OK] openapi.json généré.")

    def generate_changelog():
        with open("CHANGELOG.md", "a", encoding="utf-8") as f:
            f.write(f"\n## {datetime.date.today()} - Projet généré/modifié\n")
        with open("version.txt", "w", encoding="utf-8") as v:
            v.write(datetime.date.today().isoformat())
        add_log("[OK] CHANGELOG et version.txt générés.")

    def reset_git():
        if os.path.isdir(".git"):
            import shutil
            shutil.rmtree(".git")
        os.system("git init")
        add_log("[GIT] Dépôt Git réinitialisé.")

    def push_github():
        add_log("[GIT] Simu push (à brancher sur Git réel)")
        messagebox.showinfo("GitHub", "Push simulé !")

    def open_github_repo():
        url = "https://github.com/TON-UTILISATEUR/TON-DEPOT"
        import webbrowser
        webbrowser.open(url)
        add_log("[GIT] Ouverture page GitHub.")

    def save_profile(profile_name="Default"):
        profiles = {}
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                profiles = json.load(f)
        profiles[profile_name] = {
            "date": datetime.datetime.now().isoformat()
        }
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2)
        add_log(f"[PROFIL] Profil '{profile_name}' sauvegardé.")

    def load_profile(profile_name="Default"):
        if not os.path.exists(PROFILES_FILE):
            add_log("[PROFIL] Aucun profil à charger.")
            return
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            profiles = json.load(f)
        if profile_name not in profiles:
            add_log(f"[PROFIL] Profil '{profile_name}' introuvable.")
            return
        add_log(f"[PROFIL] Profil '{profile_name}' chargé.")

    def save_ia_history(prompt, response):
        history = []
        if os.path.exists(HIST_FILE):
            with open(HIST_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        history.append({"prompt": prompt, "response": response})
        with open(HIST_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    # ---------- UI Projet ----------
    proj_frame = tb.LabelFrame(tab_project, text="Actions Projet", bootstyle="primary")
    proj_frame.pack(fill="x", padx=10, pady=10)
    tb.Button(proj_frame, text="Générer Projet", command=generate_project, bootstyle="success-outline").pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Créer .code-workspace", command=generate_workspace).pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Générer README.md", command=generate_project).pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Générer OpenAPI", command=generate_openapi).pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Générer CHANGELOG / version", command=generate_changelog).pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Flasher ESP32 (auto COM)", command=flash_esp32, bootstyle="warning-outline").pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Sauver Profil", command=lambda: save_profile("Default")).pack(fill="x", pady=2)
    tb.Button(proj_frame, text="Réinitialiser Git", command=reset_git).pack(fill="x", pady=2)
    # --------- LVGL/HARDWARE --------
    tb.Button(proj_frame, text="LVGL Home", command=lambda: send_serial_command("LVGL:HOME"), bootstyle="info-outline").pack(fill="x", pady=2)
    tb.Button(proj_frame, text="LVGL Next", command=lambda: send_serial_command("LVGL:NEXT")).pack(fill="x", pady=2)

    # ---------- UI Git ----------
    git_frame = tb.LabelFrame(tab_git, text="Gestion GitHub", bootstyle="secondary")
    git_frame.pack(fill="x", padx=10, pady=10)
    tb.Button(git_frame, text="Push GitHub", command=push_github).pack(fill="x", pady=2)
    tb.Button(git_frame, text="Ouvrir Page GitHub", command=open_github_repo).pack(fill="x", pady=2)

    # ---------- UI IA (OpenAI réelle) ----------
    ia_frame = tb.LabelFrame(tab_ia, text="Assistant IA (OpenAI Codex)", bootstyle="success")
    ia_frame.pack(fill="x", padx=10, pady=10)

    api_key_entry = tb.Entry(ia_frame, width=60, show="*")
    api_key_entry.insert(0, "sk-...") # Mets ta clé ici ou saisis-la dans l’UI
    api_key_entry.pack(side="top", padx=2, pady=2)

    prompt_entry = tb.Entry(ia_frame, width=70)
    prompt_entry.pack(side="left", padx=2, pady=2)
    def call_ia():
        prompt = prompt_entry.get()
        api_key = api_key_entry.get()
        if not prompt or not api_key:
            messagebox.showerror("Erreur", "Prompt ou clé API manquant !")
            return
        try:
            import requests
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100
            }
            r = requests.post(url, headers=headers, json=data)
            result = r.json()
            if "error" in result:
                raise Exception(result["error"]["message"])
            response = result["choices"][0]["message"]["content"]
        except Exception as e:
            response = f"[Erreur API] {e}"
        save_ia_history(prompt, response)
        add_log(f"[IA] {response}")
        messagebox.showinfo("Réponse IA", response)
    tb.Button(ia_frame, text="Prompt IA (API OpenAI)", command=call_ia, bootstyle="success-outline").pack(side="left", padx=2, pady=2)

    # ---------- UI Outils avancés ----------
    tools_frame = tb.LabelFrame(tab_tools, text="Outils avancés", bootstyle="warning")
    tools_frame.pack(fill="x", padx=10, pady=10)
    tb.Button(tools_frame, text="Menu GitHub Actions CI/CD", command=lambda: add_log("[CI/CD] Menu lancé")).pack(fill="x", pady=2)

    add_log("DevCenter PRO initialisé. UI moderne + hardware + IA.")
    app.mainloop()

if __name__ == "__main__":
    threading.Thread(target=run_app).start()
