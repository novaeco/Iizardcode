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

---

## 🏷️ Personnalisation

- **Logo personnalisable** :  
    - Remplace `logo.ico` par ton icône, ou modifie la ligne dans `main.py` :  
      ```python
      app.iconbitmap('logo.ico')  # Change le nom ici si besoin
      ```
    - Ajoute un logo dans le README via `![Logo](tonlogo.png)` si tu préfères un PNG (et update le chemin)
- **Branding** :  
    - Change la bannière de l’UI dans `main.py`  
    - Ajoute ton nom dans le footer, et dans ce README  
    - Modifie l’URL du dépôt si besoin

---

## 📝 Installation rapide

### .EXE (auto-détection Python)
- Double-clique sur `DevCenter.exe`  
- Python sera installé automatiquement si absent

### .PY
- Installe Python : https://www.python.org/downloads/
- Puis, dans le dossier :
    ```bash
    pip install ttkbootstrap
    python main.py
    ```
- **Optionnel** : Installe `pyserial` si tu veux la détection de port COM pour ESP32 :  
    ```bash
    pip install pyserial
    ```

---

## 📂 Structure

DevCenter/
├── main.py
├── logo.ico # Ton logo, à personnaliser !
├── agents.json
├── [autres fichiers]

yaml
Copier
Modifier

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