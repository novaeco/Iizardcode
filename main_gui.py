import sys, os, datetime, json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading

# --- Dépendances non bloquantes : on log au lieu de planter
try:
    import requests
except ImportError:
    requests = None
try:
    import serial.tools.list_ports
except ImportError:
    serial = None

# ---------- FICHIERS ----------
PROFILES_FILE = "profiles.json"
HIST_FILE = "historique_ia.json"
OPENAPI_FILE = "openapi.json"

# ---------- UI PRINCIPALE ----------
def run_app():
    app = tk.Tk()
    app.title("DevCenter PRO (Final, NoFail)")
    app.geometry("1200x900")
    app.configure(bg="#f6f6f8")

    # ----- LOGS -----
    log_frame = ttk.LabelFrame(app, text="🪵 Logs en direct", padding=10)
    log_frame.pack(fill="both", expand=False, padx=10, pady=5)
    log_box = scrolledtext.ScrolledText(log_frame, height=8, font=("Consolas", 9), state="disabled", bg="#ffffff")
    log_box.pack(fill="both", expand=True)
    def add_log(msg):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        log_box.config(state="normal")
        log_box.insert("end", f"[{now}] {msg}\n")
        log_box.config(state="disabled")
        log_box.see("end")

    # ----- TABS -----
    main_frame = ttk.Notebook(app)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)
    tab_project = ttk.Frame(main_frame)
    tab_ia = ttk.Frame(main_frame)
    tab_git = ttk.Frame(main_frame)
    tab_tools = ttk.Frame(main_frame)
    main_frame.add(tab_project, text="📦 Projet")
    main_frame.add(tab_ia, text="🤖 Assistant IA")
    main_frame.add(tab_git, text="📤 GitHub")
    main_frame.add(tab_tools, text="🛠️ Outils avancés")

    # ---------- FONCTIONS (SÛRES) ----------

    def detect_com():
        if serial is None:
            add_log("[ERR] pyserial absent, COM indisponible")
            messagebox.showwarning("ESP32", "pyserial n'est pas installé !")
            return None
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            add_log("[ERR] Aucun port COM détecté")
            messagebox.showwarning("ESP32", "Aucun port COM détecté !")
            return None
        add_log(f"[OK] Port détecté : {ports[0].device}")
        return ports[0].device

    def flash_esp32():
        port = detect_com()
        if not port:
            return
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

    # ---------- UI -----------

    proj_frame = ttk.LabelFrame(tab_project, text="Actions Projet", padding=10)
    proj_frame.pack(fill="x", padx=10, pady=10)
    ttk.Button(proj_frame, text="Générer Projet", command=generate_project).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Créer .code-workspace", command=generate_workspace).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Générer README.md", command=generate_project).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Générer OpenAPI", command=generate_openapi).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Générer CHANGELOG / version", command=generate_changelog).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Flasher ESP32 (auto COM)", command=flash_esp32).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Sauver Profil", command=lambda: save_profile("Default")).pack(fill="x", pady=2)
    ttk.Button(proj_frame, text="Réinitialiser Git", command=reset_git).pack(fill="x", pady=2)

    git_frame = ttk.LabelFrame(tab_git, text="Gestion GitHub", padding=10)
    git_frame.pack(fill="x", padx=10, pady=10)
    ttk.Button(git_frame, text="Push GitHub", command=push_github).pack(fill="x", pady=2)
    ttk.Button(git_frame, text="Ouvrir Page GitHub", command=open_github_repo).pack(fill="x", pady=2)

    ia_frame = ttk.LabelFrame(tab_ia, text="Assistant IA (OpenAI Codex)", padding=10)
    ia_frame.pack(fill="x", padx=10, pady=10)

    prompt_entry = ttk.Entry(ia_frame, width=70)
    prompt_entry.pack(side="left", padx=2, pady=2)
    def call_ia():
        prompt = prompt_entry.get()
        if not prompt:
            return
        response = "[Simulation IA] Réponse à : " + prompt
        save_ia_history(prompt, response)
        add_log(f"[IA] {response}")
        messagebox.showinfo("Réponse IA", response)
    ttk.Button(ia_frame, text="Prompt IA", command=call_ia).pack(side="left", padx=2, pady=2)

    tools_frame = ttk.LabelFrame(tab_tools, text="Outils avancés", padding=10)
    tools_frame.pack(fill="x", padx=10, pady=10)
    ttk.Button(tools_frame, text="Menu GitHub Actions CI/CD", command=lambda: add_log("[CI/CD] Menu lancé")).pack(fill="x", pady=2)

    add_log("DevCenter PRO initialisé. Toutes fonctions actives.")
    app.mainloop()

# ----- Lancement asynchrone pour que la fenêtre s'affiche TOUJOURS -----
if __name__ == "__main__":
    threading.Thread(target=run_app).start()
