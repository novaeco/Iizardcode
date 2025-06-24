# 🦎 DevCenter PRO by NovaDevSysthem

**DevCenter PRO** — La solution ultime pour la gestion et l’automatisation de projets embarqués, IoT et IA.  
Développé par **NovaDevSysthem** avec l’assistance d’agents IA sur-mesure.  
![Logo](logo.ico) <!-- Ton logo ici, tu peux remplacer par ![Logo](static/tonlogo.png) si besoin -->

---

## ⚡️ Fonctions clés

- **Interface graphique moderne & multi-thèmes** (inspirée IDE 2025)
- **Gestion projet** : génération ESP32/BPI, .code-workspace, README, OpenAPI, CHANGELOG, version, dossiers, profils multiples…
- **Flash ESP32** : auto-détection port COM, console intégrée
- **Assistant IA multi-agent**
    - Création/gestion illimitée d’agents IA (source : ChatGPT, Codex, Bolt, Gemini, Mistral…)
    - Activation/désactivation, édition de chaque agent (nom, icône, IA, etc.)
    - Historique IA par projet (local, consultable)
    - **Configuration sécurisée de la clé API OpenAI**
- **GitHub intégré** : push, ouverture, reset Git, gestion Actions CI/CD
- **Documentation automatique** : README.md, OpenAPI, CHANGELOG…
- **Logs en direct** (toutes actions projet, IA, flash, build…)
- **Support multi-carte** : ESP32, ESP32‑C6, ESP32‑P4, Raspberry Pi, BPI (voir le dossier `cartes/`)

---

## 🏷️ Personnalisation

- **Logo personnalisable** :
    - Remplace `logo.ico` par ton icône, ou modifie la ligne dans `main_gui.py` :  
      ```python
      app.iconbitmap('logo.ico')  # Change le nom ici si besoin
      ```
    - Ajoute un logo dans le README via `![Logo](tonlogo.png)` si tu préfères un PNG (et update le chemin)
- **Image de démo des polices** :
    - `img-font.png` est affiché dans l'application (accueil & barre latérale).
      Remplace-le par ton propre fichier si tu souhaites personnaliser l'image.
- **Branding** :
    - Change la bannière de l’UI dans `main_gui.py`  
    - Ajoute ton nom dans le footer, et dans ce README  
    - Personnalise l’URL du dépôt via `github_repo_url` dans `config.json` pour le bouton "Ouvrir Page GitHub"

---

## 📝 Installation rapide

### .EXE (auto-détection Python)
- Double-clique sur `DevCenter.exe`  
- Python sera installé automatiquement si absent

### .PY
- Installe Python : https://www.python.org/downloads/
- Puis, dans le dossier :
    ```bash
    pip install -r requirements.txt
    python main_gui.py
    ```
La détection automatique du port COM pour ESP32 fonctionne grâce au paquet `pyserial` déjà listé dans `requirements.txt`.

### Via `pip` (pyproject)
Pour installer DevCenter comme un paquet Python :
```bash
pip install .
devcenter
```

### Générer un exécutable
Avec PyInstaller :
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed main_gui.py
```
Un script `build_exe.bat` est fourni pour Windows.

## 🔑 Configuration de la clé API OpenAI

Renseigne la clé dans `config.json` :

```json
{
  "openai_api_key": "sk-..."
}
```

Pour personnaliser le bouton "Ouvrir Page GitHub", ajoute la clé `github_repo_url` :

```json
{
  "openai_api_key": "sk-...",
  "github_repo_url": "https://github.com/moncompte/mondepot"
}
```

Tu peux aussi définir une variable d'environnement :

```bash
export OPENAI_API_KEY="sk-..."
```

Si les dépendances ne sont pas installées, l'exécution renverra l'erreur `ModuleNotFoundError: openai`.

## 🧪 Tests

Depuis la racine du projet :
```bash
pip install -r requirements.txt
pytest
```


---

## 📂 Structure

DevCenter/
├── main_gui.py
├── logo.ico # Ton logo, à personnaliser !
├── dist/agents.json
├── cartes/
│   ├── esp32/
│   ├── esp32_c6/
│   ├── esp32_p4/
│   ├── raspberry_pi/
│   └── bpi/
├── [autres fichiers]

Chaque sous-dossier dans `cartes/` regroupe la documentation minimale pour la
carte correspondante :
`esp32` et `esp32_c6` pour les déclinaisons ESP32, `esp32_p4` pour la version
P4, `raspberry_pi` pour la gamme Raspberry Pi et `bpi` pour Banana Pi.

---

## 🌟 UI & Navigation

- **Barre latérale :** Accueil, Projet, IA, GitHub, Outils
- **IA** :  
    - Liste des agents IA  
    - Créer un agent IA  
    - Paramètres IA globaux (clé API, source, etc.)
- **Projet** :  
    - Générer sources, .code-workspace, README, OpenAPI, etc.
    - Flasher ESP32 (auto COM)
    - Gestion multi-profil
    - Réinitialisation Git, push, actions CI/CD…
- **Logs live** pour tout voir

---

## 🤖 Agents IA – Usage & Branding

- Crée autant d’agents IA que tu veux (branding par icône, nom, IA connectée…)
- Choisis la source IA de chaque agent : ChatGPT, Codex, Bolt, Gemini, etc.
- Tu gères l’activation, la config, l’historique IA dans le logiciel

---

## 👨‍💻 Développé par

> NovaDevSysthem  
>
> Dépôt officiel : https://github.com/novaeco/Iizardcode.git
>  
> _Version  2025, tous droits réservés._

---

## 🦎 À toi de jouer !
Ce DevCenter est prêt à booster tes projets embarqués, IA & cloud —  
N’hésite pas à personnaliser ton branding, logo et ajouter tes agents IA favoris.