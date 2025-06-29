import os
import json
import datetime

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None
import webbrowser

PROFILES_FILE = "profiles.json"
HIST_FILE = "historique_ia.json"
OPENAPI_FILE = "openapi.json"
CONFIG_FILE = "config.json"


def generate_project():
    """Create a minimal source tree with a stub main file and README."""
    os.makedirs("src", exist_ok=True)
    with open("src/main.c", "w") as f:
        f.write("// Entry point du projet généré\nint main() { return 0; }\n")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Projet ESP32/BPI généré par DevCenter\n")
    return "[OK] Projet ESP32/BPI généré."


def generate_readme():
    """Créer uniquement le fichier README.md pour le projet."""
    content = [
        "# Projet généré avec DevCenter PRO\n",
        "\n",
        "Ce fichier README a été généré automatiquement.\n",
    ]
    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(content)
    return "[OK] README.md généré."


def generate_workspace():
    """Write a VS Code workspace file for the current project."""
    ws = {"folders": [{"path": "."}], "settings": {}}
    with open(".code-workspace", "w", encoding="utf-8") as f:
        json.dump(ws, f, indent=2)
    return "[OK] .code-workspace généré."


def generate_openapi():
    """Create a very small OpenAPI skeleton file."""
    openapi = {
        "openapi": "3.0.0",
        "info": {"title": "DevCenter API", "version": "1.0.0"},
        "paths": {},
    }
    with open(OPENAPI_FILE, "w", encoding="utf-8") as f:
        json.dump(openapi, f, indent=2)
    return "[OK] openapi.json généré."


def generate_changelog():
    """Append today's entry to CHANGELOG and update version.txt."""
    with open("CHANGELOG.md", "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.date.today()} - Projet généré/modifié\n")
    with open("version.txt", "w", encoding="utf-8") as v:
        v.write(datetime.date.today().isoformat())
    return "[OK] CHANGELOG et version.txt générés."


def detect_com():
    """Return the list of available serial ports."""
    try:
        import serial.tools.list_ports

        ports = [p.device for p in serial.tools.list_ports.comports()]
        if not ports:
            return [], "[ERR] Aucun port COM détecté"
        if len(ports) == 1:
            return ports, f"[OK] Port détecté : {ports[0]}"
        return ports, "[OK] Ports détectés : " + ", ".join(ports)
    except Exception as e:
        return [], f"[ERR] pyserial absent ou erreur : {e}"


def flash_esp32(port=None):
    """Fake flashing of an ESP32 using the detected port."""
    ports, log = detect_com()
    if not ports:
        return log
    if port is None:
        if len(ports) == 1:
            port = ports[0]
        else:
            return f"[ERR] Plusieurs ports disponibles : {', '.join(ports)}"
    return f"[FLASH] (Fake) Flash ESP32 sur {port}"


def reset_git():
    """Remove any existing Git repository and reinitialise it."""
    if os.path.isdir(".git"):
        import shutil

        shutil.rmtree(".git")
    os.system("git init")
    return "[GIT] Dépôt Git réinitialisé."


def push_github():
    """Placeholder for pushing the project to GitHub."""
    return "[GIT] Simu push (à brancher sur Git réel)"


def open_github_repo(url=None):
    """Ouvre le dépôt GitHub défini dans config.json ou celui passé en param."""
    if url is None:
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                url = json.load(f).get("github_repo_url")
        except Exception:
            url = None
    if not url:
        url = "https://github.com/TON-UTILISATEUR/TON-DEPOT"
    webbrowser.open(url)
    return "[GIT] Ouverture page GitHub."


def save_profile(profile_name="Default"):
    """Persist simple metadata about the current user profile."""
    profiles = {}
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            profiles = json.load(f)
    profiles[profile_name] = {"date": datetime.datetime.now().isoformat()}
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)
    return f"[PROFIL] Profil '{profile_name}' sauvegardé."


def load_profile(profile_name="Default"):
    """Return saved profile data or None if not found."""
    if not os.path.exists(PROFILES_FILE):
        return None
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles = json.load(f)
    return profiles.get(profile_name)


def list_profiles():
    """Return the list of saved profile names."""
    if not os.path.exists(PROFILES_FILE):
        return []
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        return list(json.load(f).keys())


def load_config():
    """Load configuration from CONFIG_FILE or return empty dict."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    """Write configuration dictionary to CONFIG_FILE."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return "[OK] Config sauvegardée."


def save_ia_history(prompt, response):
    """Append a question/answer pair to the local history file."""
    history = []
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    history.append({"prompt": prompt, "response": response})
    with open(HIST_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def ask_openai(prompt):
    """Envoie le prompt à l'API OpenAI et renvoie la réponse."""
    if openai is None:  # pragma: no cover - optional dependency
        raise RuntimeError("Module 'openai' non installé")
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        api_key = config.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Clé API OpenAI manquante")
        openai.api_key = api_key
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        answer = resp.choices[0].message.content.strip()
        save_ia_history(prompt, answer)
        return answer
    except Exception as e:
        raise RuntimeError(f"Erreur réseau/IA : {e}")
