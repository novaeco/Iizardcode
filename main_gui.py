import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import threading, os, datetime, json
from hardware import send_serial_command

PROFILES_FILE = "profiles.json"
HIST_FILE = "historique_ia.json"
OPENAPI_FILE = "openapi.json"

def generate_project():
    os.makedirs("src", exist_ok=True)
    with open("src/main.c", "w") as f:
        f.write("// Entry point du projet généré\nint main() { return 0; }\n")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Projet ESP32/BPI généré par DevCenter\n")
    return "[OK] Projet ESP32/BPI généré."

def generate_workspace():
    ws = {"folders": [{"path": "."}], "settings": {}}
    with open(".code-workspace", "w", encoding="utf-8") as f:
        json.dump(ws, f, indent=2)
    return "[OK] .code-workspace généré."

def generate_openapi():
    openapi = {
        "openapi": "3.0.0",
        "info": {"title": "DevCenter API", "version": "1.0.0"},
        "paths": {}
    }
    with open(OPENAPI_FILE, "w", encoding="utf-8") as f:
        json.dump(openapi, f, indent=2)
    return "[OK] openapi.json généré."

def generate_changelog():
    with open("CHANGELOG.md", "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.date.today()} - Projet généré/modifié\n")
    with open("version.txt", "w", encoding="utf-8") as v:
        v.write(datetime.date.today().isoformat())
    return "[OK] CHANGELOG et version.txt générés."

def detect_com():
    try:
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            return None, "[ERR] Aucun port COM détecté"
        return ports[0].device, f"[OK] Port détecté : {ports[0].device}"
    except Exception as e:
        return None, f"[ERR] pyserial absent ou erreur : {e}"

def flash_esp32():
    port, log = detect_com()
    if not port:
        return log
    # À adapter : ici on simule le flash
    return f"[FLASH] (Fake) Flash ESP32 sur {port}"

def reset_git():
    if os.path.isdir(".git"):
        import shutil
        shutil.rmtree(".git")
    os.system("git init")
    return "[GIT] Dépôt Git réinitialisé."

def push_github():
    # À brancher sur git réel si besoin
    return "[GIT] Simu push (à brancher sur Git réel)"

def open_github_repo():
    url = "https://github.com/TON-UTILISATEUR/TON-DEPOT"
    import webbrowser
    webbrowser.open(url)
    return "[GIT] Ouverture page GitHub."

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
    return f"[PROFIL] Profil '{profile_name}' sauvegardé."

def load_profile(profile_name="Default"):
    if not os.path.exists(PROFILES_FILE):
        return "[PROFIL] Aucun profil à charger."
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles = json.load(f)
    if profile_name not in profiles:
        return f"[PROFIL] Profil '{profile_name}' introuvable."
    return f"[PROFIL] Profil '{profile_name}' chargé."

def save_ia_history(prompt, response):
    history = []
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    history.append({"prompt": prompt, "response": response})
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def run_app():
    app = tb.Window(themename="darkly")
    app.title("DevCenter PRO – UI finale")
    app.geometry("1280x800")
    app.resizable(True, True)

    # ===== Layout général : barre latérale + contenu principal =====
    root_frame = tb.Frame(app)
    root_frame.pack(fill="both", expand=True)

    # --- Barre latérale ---
    sidebar = tb.Frame(root_frame, width=220, bootstyle="secondary")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tb.Label(sidebar, text="🚀 DevCenter PRO", font=("Arial", 16, "bold"), bootstyle="inverse-secondary").pack(pady=(30, 15))
    tb.Label(sidebar, text="Développement • ESP32 • IA", font=("Arial", 10), bootstyle="inverse-secondary").pack(pady=(0, 20))

    nav = {}
    def show_panel(name):
        for n, fr in nav.items():
            fr.pack_forget()
        nav[name].pack(fill="both", expand=True)
    nav_btns = [
        ("Accueil", lambda: show_panel("accueil")),
        ("Projet", lambda: show_panel("projet")),
        ("IA", lambda: show_panel("ia")),
        ("GitHub", lambda: show_panel("git")),
        ("Outils", lambda: show_panel("tools"))
    ]
    for txt, cmd in nav_btns:
        tb.Button(sidebar, text=txt, width=20, command=cmd, bootstyle="secondary-outline").pack(pady=4, padx=10)
    tb.Label(sidebar, text="", bootstyle="inverse-secondary").pack(expand=True, fill="y")
    tb.Label(sidebar, text="by NovaDevSysthem", font=("Arial", 8), bootstyle="inverse-secondary").pack(pady=12)

    # === Zone principale (contenu dynamique) ===
    content = tb.Frame(root_frame)
    content.pack(side="right", fill="both", expand=True)

    # --- LOGS haut ---
    log_frame = tb.Labelframe(content, text="🪵 Logs en direct", bootstyle="info")
    log_frame.pack(fill="x", padx=16, pady=(10, 0))
    log_box = scrolledtext.ScrolledText(log_frame, height=6, font=("Consolas", 9), state="disabled")
    log_box.pack(fill="x")
    def add_log(msg):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        log_box.config(state="normal")
        log_box.insert("end", f"[{now}] {msg}\n")
        log_box.config(state="disabled")
        log_box.see("end")

    # --- PANELS DE FONCTIONS ---
    accueil_panel = tb.Frame(content)
    tb.Label(accueil_panel, text="Bienvenue sur DevCenter PRO", font=("Arial", 20, "bold")).pack(pady=40)
    tb.Label(accueil_panel, text="Sélectionne une section dans la barre latérale.", font=("Arial", 12)).pack()
    nav["accueil"] = accueil_panel

    projet_panel = tb.Frame(content)
    tb.Label(projet_panel, text="Génération & gestion du projet", font=("Arial", 15, "bold")).pack(pady=12)
    tb.Button(projet_panel, text="Générer Projet", command=lambda: add_log(generate_project())).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="Créer .code-workspace", command=lambda: add_log(generate_workspace())).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="Générer README.md", command=lambda: add_log(generate_project())).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="Générer OpenAPI", command=lambda: add_log(generate_openapi())).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="Générer CHANGELOG / version", command=lambda: add_log(generate_changelog())).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="Flasher ESP32 (auto COM)", command=lambda: add_log(flash_esp32())).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="LVGL Home", command=lambda: add_log("LVGL:HOME envoyé" if send_serial_command("LVGL:HOME") else "Erreur LVGL:HOME")).pack(fill="x", padx=100, pady=4)
    tb.Button(projet_panel, text="LVGL Next", command=lambda: add_log("LVGL:NEXT envoyé" if send_serial_command("LVGL:NEXT") else "Erreur LVGL:NEXT")).pack(fill="x", padx=100, pady=4)
    nav["projet"] = projet_panel

    ia_panel = tb.Frame(content)
    tb.Label(ia_panel, text="Assistant IA (OpenAI)", font=("Arial", 15, "bold")).pack(pady=12)
    api_key_entry = tb.Entry(ia_panel, width=60, show="*")
    api_key_entry.insert(0, "sk-...")
    api_key_entry.pack(pady=3)
    prompt_entry = tb.Entry(ia_panel, width=80)
    prompt_entry.pack(pady=3)
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
    tb.Button(ia_panel, text="Prompt IA (API OpenAI)", command=call_ia, bootstyle="success-outline").pack(pady=5)
    nav["ia"] = ia_panel

    git_panel = tb.Frame(content)
    tb.Label(git_panel, text="Intégration GitHub", font=("Arial", 15, "bold")).pack(pady=12)
    tb.Button(git_panel, text="Push GitHub", command=lambda: add_log(push_github())).pack(fill="x", padx=120, pady=4)
    tb.Button(git_panel, text="Ouvrir Page GitHub", command=lambda: add_log(open_github_repo())).pack(fill="x", padx=120, pady=4)
    nav["git"] = git_panel

    tools_panel = tb.Frame(content)
    tb.Label(tools_panel, text="Outils avancés / CI/CD", font=("Arial", 15, "bold")).pack(pady=12)
    tb.Button(tools_panel, text="Menu GitHub Actions CI/CD", command=lambda: add_log("[CI/CD] Menu lancé")).pack(fill="x", padx=120, pady=4)
    nav["tools"] = tools_panel

    show_panel("accueil")
    add_log("DevCenter PRO initialisé. UI finale, tout rangé.")
    app.mainloop()

if __name__ == "__main__":
    threading.Thread(target=run_app).start()
