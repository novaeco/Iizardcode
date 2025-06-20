import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
import threading, os, datetime, json

PROFILES_FILE = "profiles.json"
HIST_FILE = "historique_ia.json"
OPENAPI_FILE = "openapi.json"
AGENTS_FILE = "agents.json"
THEMES = [
    "darkly", "flatly", "cyborg", "superhero", "minty", "journal", "yeti"
]

IA_SOURCES = [
    "ChatGPT", "Codex", "Bolt", "Mistral", "Gemini"
]

def load_agents():
    if not os.path.exists(AGENTS_FILE):
        return []
    with open(AGENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_agents(agents):
    with open(AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(agents, f, indent=2, ensure_ascii=False)

def create_or_edit_agent_window(parent, on_saved, agent=None):
    top = tb.Toplevel(parent)
    top.title("Configurer Agent IA" if agent else "Créer un nouvel Agent IA")
    tb.Label(top, text="Nom de l’agent :").pack(pady=5)
    name_entry = tb.Entry(top, width=40)
    name_entry.insert(0, agent["name"] if agent else "")
    name_entry.pack(pady=2)
    tb.Label(top, text="Icône (ex: 🤖):").pack(pady=5)
    icon_entry = tb.Entry(top, width=8)
    icon_entry.insert(0, agent["icon"] if agent else "")
    icon_entry.pack(pady=2)
    tb.Label(top, text="Source IA :").pack(pady=5)
    source_box = tb.Combobox(top, values=IA_SOURCES, width=22)
    source_box.set(agent.get("ia_source", IA_SOURCES[0]) if agent else IA_SOURCES[0])
    source_box.pack(pady=2)
    def submit():
        name = name_entry.get().strip()
        icon = icon_entry.get().strip() or "🤖"
        ia_source = source_box.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Nom obligatoire")
            return
        d = {
            "name": name,
            "role": name.replace(" ", "_").lower(),
            "icon": icon,
            "active": agent["active"] if agent else True,
            "ia_source": ia_source
        }
        on_saved(d)
        top.destroy()
    tb.Button(top, text="Enregistrer", command=submit, bootstyle="success").pack(pady=10)

def ia_tab_panel(parent):
    frame = tb.Frame(parent)
    agents = load_agents()

    # Barre de navigation IA (3 boutons)
    nav_frame = tb.Frame(frame)
    nav_frame.pack(fill="x", pady=6)

    section = tb.StringVar(value="agents")

    def show_section(sec):
        section.set(sec)
        refresh_body()

    tb.Button(nav_frame, text="👥 Agents IA", width=16, bootstyle="info" if section.get()=="agents" else "secondary", command=lambda: show_section("agents")).pack(side="left", padx=3)
    tb.Button(nav_frame, text="➕ Créer un Agent IA", width=18, bootstyle="success" if section.get()=="create" else "secondary", command=lambda: show_section("create")).pack(side="left", padx=3)
    tb.Button(nav_frame, text="⚙️ Paramètres IA", width=16, bootstyle="warning" if section.get()=="params" else "secondary", command=lambda: show_section("params")).pack(side="left", padx=3)

    # Conteneur dynamique pour la section
    body = tb.Frame(frame)
    body.pack(fill="both", expand=True, padx=7, pady=8)

    def refresh_agents_list():
        for w in body.winfo_children():
            w.destroy()
        if not agents:
            tb.Label(body, text="Aucun agent IA créé.", font=("Segoe UI", 12, "italic")).pack()
            return
        for idx, ag in enumerate(agents):
            status = "🟢" if ag.get("active", False) else "⚪"
            ag_frame = tb.Frame(body)
            ag_frame.pack(fill="x", pady=2)
            tb.Label(ag_frame, text=f"{ag['icon']} {ag['name']}", font=("Segoe UI", 12, "bold")).pack(side="left")
            tb.Label(ag_frame, text=f"Rôle: {ag['role']}", font=("Segoe UI", 10)).pack(side="left", padx=10)
            tb.Label(ag_frame, text=f"IA: {ag.get('ia_source', 'N/A')}", font=("Segoe UI", 10, "italic")).pack(side="left", padx=8)
            tb.Label(ag_frame, text=f"{status} ", font=("Segoe UI", 14)).pack(side="right")
            def toggle(idx=idx):
                agents[idx]["active"] = not agents[idx].get("active", False)
                save_agents(agents)
                refresh_body()
            tb.Button(ag_frame, text="Activer/Désactiver", command=toggle, width=13, bootstyle="secondary").pack(side="right", padx=4)
            def edit(idx=idx):
                create_or_edit_agent_window(
                    frame,
                    lambda new_ag: (
                        agents.__setitem__(idx, {**agents[idx], **new_ag}),
                        save_agents(agents),
                        refresh_body()
                    ),
                    agent=agents[idx]
                )
            tb.Button(ag_frame, text="Modifier", command=edit, width=8, bootstyle="info-outline").pack(side="right", padx=3)

    def refresh_create_agent():
        for w in body.winfo_children():
            w.destroy()
        create_or_edit_agent_window(
            body,
            lambda ag: (agents.append(ag), save_agents(agents), show_section("agents")),
            agent=None
        )

    def refresh_params():
        for w in body.winfo_children():
            w.destroy()
        tb.Label(body, text="Paramètres de tous les agents IA", font=("Segoe UI", 14, "bold")).pack(pady=7)
        for idx, ag in enumerate(agents):
            param_frame = tb.Labelframe(body, text=f"{ag['icon']} {ag['name']}", bootstyle="warning")
            param_frame.pack(fill="x", pady=3, padx=10)
            tb.Label(param_frame, text="Nom:").grid(row=0, column=0, sticky="w")
            name_var = tb.StringVar(value=ag["name"])
            name_entry = tb.Entry(param_frame, textvariable=name_var, width=22)
            name_entry.grid(row=0, column=1, padx=3)
            tb.Label(param_frame, text="Icône:").grid(row=0, column=2)
            icon_var = tb.StringVar(value=ag["icon"])
            icon_entry = tb.Entry(param_frame, textvariable=icon_var, width=4)
            icon_entry.grid(row=0, column=3, padx=3)
            tb.Label(param_frame, text="Source IA:").grid(row=0, column=4)
            source_var = tb.StringVar(value=ag.get("ia_source", "ChatGPT"))
            source_box = tb.Combobox(param_frame, textvariable=source_var, values=IA_SOURCES, width=11)
            source_box.grid(row=0, column=5, padx=4)
            def save(idx=idx, name_var=name_var, icon_var=icon_var, source_var=source_var):
                agents[idx]["name"] = name_var.get()
                agents[idx]["icon"] = icon_var.get()
                agents[idx]["ia_source"] = source_var.get()
                save_agents(agents)
                refresh_body()
            tb.Button(param_frame, text="Enregistrer", command=save, bootstyle="success-outline").grid(row=0, column=6, padx=8)
    def refresh_body():
        if section.get() == "agents":
            refresh_agents_list()
        elif section.get() == "create":
            refresh_create_agent()
        elif section.get() == "params":
            refresh_params()
    refresh_body()
    return frame
# --- AUTRES MODULES / OUTILS ---
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
    return f"[FLASH] (Fake) Flash ESP32 sur {port}"

def reset_git():
    if os.path.isdir(".git"):
        import shutil
        shutil.rmtree(".git")
    os.system("git init")
    return "[GIT] Dépôt Git réinitialisé."

def push_github():
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

def save_ia_history(prompt, response):
    history = []
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    history.append({"prompt": prompt, "response": response})
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def run_app():
    themename = "darkly"
    app = tb.Window(themename=themename)
    app.title("DevCenter PRO – Ultimate UI")
    app.geometry("1320x820")
    app.iconbitmap('logo.ico')   # Icône personnalisée

    # Theme switcher
    def set_theme(theme):
        nonlocal themename
        themename = theme
        app.style.theme_use(themename)
        add_log(f"[UI] Thème changé: {theme}")

    # Barre latérale
    root_frame = tb.Frame(app)
    root_frame.pack(fill="both", expand=True)

    sidebar = tb.Frame(root_frame, width=230, bootstyle="secondary")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    tb.Label(sidebar, text="🚀 DevCenter PRO", font=("Segoe UI", 17, "bold"), bootstyle="inverse-secondary").pack(pady=(30, 10))
    tb.Label(sidebar, text="Automatisation · IoT · IA", font=("Segoe UI", 10), bootstyle="inverse-secondary").pack(pady=(0, 18))
    # Sélecteur de thème
    tb.Label(sidebar, text="🎨 Thème", font=("Segoe UI", 10, "bold"), bootstyle="inverse-secondary").pack(pady=(0, 0))
    theme_box = tb.Combobox(sidebar, values=THEMES, width=18)
    theme_box.set(themename)
    theme_box.pack(pady=(0, 15))
    theme_box.bind("<<ComboboxSelected>>", lambda e: set_theme(theme_box.get()))

    nav = {}
    def show_panel(name):
        for n, fr in nav.items():
            fr.pack_forget()
        nav[name].pack(fill="both", expand=True)
    nav_btns = [
        ("🏠 Accueil", lambda: show_panel("accueil")),
        ("🗂️ Projet", lambda: show_panel("projet")),
        ("🤖 IA", lambda: show_panel("ia")),
        ("🌐 GitHub", lambda: show_panel("git")),
        ("⚙️ Outils", lambda: show_panel("tools"))
    ]
    for txt, cmd in nav_btns:
        tb.Button(sidebar, text=txt, width=20, command=cmd, bootstyle="secondary-outline").pack(pady=5, padx=11)

    tb.Label(sidebar, text="", bootstyle="inverse-secondary").pack(expand=True, fill="y")
    tb.Label(sidebar, text="v2025 • NovaDevSysthem", font=("Segoe UI", 8), bootstyle="inverse-secondary").pack(pady=10)

    # Contenu principal
    content = tb.Frame(root_frame)
    content.pack(side="right", fill="both", expand=True)

    log_frame = tb.Labelframe(content, text="🪵 Logs en direct", bootstyle="info")
    log_frame.pack(fill="x", padx=18, pady=(12, 2))
    log_box = scrolledtext.ScrolledText(log_frame, height=6, font=("Consolas", 9), state="disabled")
    log_box.pack(fill="x")
    def add_log(msg):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        log_box.config(state="normal")
        log_box.insert("end", f"[{now}] {msg}\n")
        log_box.config(state="disabled")
        log_box.see("end")

    # PANELS
    accueil_panel = tb.Frame(content)
    tb.Label(accueil_panel, text="Bienvenue sur DevCenter PRO", font=("Segoe UI", 23, "bold")).pack(pady=48)
    tb.Label(accueil_panel, text="Choisissez une section à gauche.", font=("Segoe UI", 13)).pack()
    nav["accueil"] = accueil_panel

    projet_panel = tb.Frame(content)
    tb.Label(projet_panel, text="🗂️ Génération & gestion du projet", font=("Segoe UI", 15, "bold")).pack(pady=14)
    tb.Button(projet_panel, text="🛠️ Générer Projet", command=lambda: add_log(generate_project()), bootstyle="success-outline").pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="📁 Créer .code-workspace", command=lambda: add_log(generate_workspace())).pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="📖 Générer README.md", command=lambda: add_log(generate_project())).pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="📘 Générer OpenAPI", command=lambda: add_log(generate_openapi())).pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="📝 Générer CHANGELOG / version", command=lambda: add_log(generate_changelog())).pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="⚡ Flasher ESP32 (auto COM)", command=lambda: add_log(flash_esp32()), bootstyle="warning-outline").pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="💾 Sauver Profil", command=lambda: add_log(save_profile())).pack(fill="x", padx=120, pady=3)
    tb.Button(projet_panel, text="🧹 Réinitialiser Git", command=lambda: add_log(reset_git())).pack(fill="x", padx=120, pady=3)
    from ttkbootstrap import Separator
    Separator(projet_panel, orient="horizontal").pack(fill="x", pady=12)
    nav["projet"] = projet_panel

    # --- NOUVEAU PANEL IA : barre navigation & options ---
    nav["ia"] = ia_tab_panel(content)

    git_panel = tb.Frame(content)
    tb.Label(git_panel, text="🌐 Intégration GitHub", font=("Segoe UI", 15, "bold")).pack(pady=14)
    tb.Button(git_panel, text="⬆️ Push GitHub", command=lambda: add_log(push_github())).pack(fill="x", padx=150, pady=3)
    tb.Button(git_panel, text="🔗 Ouvrir Page GitHub", command=lambda: add_log(open_github_repo())).pack(fill="x", padx=150, pady=3)
    nav["git"] = git_panel

    tools_panel = tb.Frame(content)
    tb.Label(tools_panel, text="⚙️ Outils avancés / CI/CD", font=("Segoe UI", 15, "bold")).pack(pady=18)
    tb.Label(tools_panel, text="À venir : intégration directe CI/CD, gestion multi-carte...", font=("Segoe UI", 11, "italic")).pack()
    nav["tools"] = tools_panel

    # Affichage initial
    show_panel("accueil")
    app.mainloop()

if __name__ == "__main__":
    run_app()
