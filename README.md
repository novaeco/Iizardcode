# 🚀 DevCenter PRO – Ultimate Embedded & AI Development Studio

**DevCenter PRO** est une plateforme graphique tout-en-un pour la génération, la gestion et l’automatisation de projets embarqués, IoT, et IA, avec support complet ESP32, BPI, GitHub, et assistants IA connectés.

---

## 🟢 Fonctionnalités principales

- **Interface moderne et réactive** (ttkbootstrap, multi-thèmes)
- **Génération de projet ESP32/BPI** clé en main (`src/`, `main.c`, `.code-workspace`, `README.md`)
- **Détection automatique du port COM** pour flash ESP32
- **Auto-flash ESP32** (détection série, simulation)
- **Gestion multi-profil** : création, sauvegarde et bascule de profils utilisateur/projet
- **Logs en direct** pour toutes les opérations (build, flash, push, IA, etc.)
- **Assistant IA intégré** :
    - Création illimitée d’agents IA (personnalisés, chacun connecté à l’IA de ton choix : ChatGPT, Codex, Bolt, Mistral, Gemini…)
    - Gestion (activation/désactivation) et édition des agents IA
    - Paramétrage de tous les agents (nom, icône, source IA) via un panneau moderne
    - Historique IA par projet (prompts/réponses sauvegardés localement)
- **Intégration GitHub** :
    - Push direct, ouverture du dépôt, détection d’erreurs
    - Bouton de réinitialisation Git
    - Générateur automatique de README, OpenAPI, CHANGELOG, version.txt
    - Gestion CI/CD (GitHub Actions, menu dédié)
- **Système de documentation API (OpenAPI)** intégré

---

## 🖥️ Installation & Prérequis

### ▶️ **Lancement rapide (.exe auto-détection)**
- Double-clique simplement sur `DevCenter.exe`  
  _→ Si Python n’est pas détecté, l’installeur le propose automatiquement_

### ▶️ **Lancement manuel (.py)**
1. **Prérequis** :  
   - Windows 10/11  
   - Python 3.8+  
   - pip install `ttkbootstrap` (`pip install ttkbootstrap`)
2. Placez `main.py`, `logo.ico` et les fichiers `.json` du projet dans un même dossier
3. Lancez via :  
   ```bash
   python main.py
▶️ Dépendances auto-gérées :
ttkbootstrap (interface)

pyserial (pour la détection COM/ESP32)

Python standard libs (json, os, etc.)

📦 Arborescence du projet
pgsql
Copier
Modifier
DevCenter/
│
├── main.py
├── logo.ico
├── agents.json
├── profiles.json
├── historique_ia.json
├── openapi.json
│
├── src/
│   └── main.c
│
├── .code-workspace
├── README.md
├── CHANGELOG.md
├── version.txt
│
└── [autres fichiers générés]
🎨 Présentation de l’interface
Barre latérale navigation :

Accueil, Projet, IA, GitHub, Outils

Onglet Projet :

Générer projet, .code-workspace, README, OpenAPI, CHANGELOG, Flasher ESP32, Sauver profil, Réinit Git, etc.

Onglet IA (nouvelle UI pro) :

Agents IA (liste, activer/désactiver, modifier)

Créer un Agent IA (formulaire complet)

Paramètres IA (édition en masse de tous les agents, choix source IA : ChatGPT/Codex/Bolt/Mistral/Gemini…)

Onglet GitHub :

Push, ouverture du dépôt, reset Git, setup Actions CI/CD, etc.

Système de logs en direct pour toutes les actions

🤖 Assistant IA intégré (fonctionnalités avancées)
Crée autant d’agents IA que tu veux (nom, icône, IA connectée, etc.)

Pour chaque agent, choisis :

Source IA : ChatGPT, Codex, Bolt, Mistral, Gemini…

Statut actif/inactif

Modification à tout moment via “Paramètres IA”

Les prompts et réponses sont archivés dans historique_ia.json

L’intégration d’API OpenAI nécessite une clé API (paramétrable, sécurité assurée)

🛡️ Sécurité & données
Toutes les données locales sont stockées en .json (agents, historique IA, profils…)

Aucun envoi externe sans action de l’utilisateur (API IA = usage opt-in avec clé)

⚡ Support matériel (ESP32, BPI-F3 K1, etc.)
Détection automatique du port COM pour flash

Génération de template projet (C/C++, ESP-IDF, .code-workspace)

Prêt pour extensions hardware (LVGL, automatisation IoT, etc.)

📢 Astuces & Tips
Si un agent IA ne fonctionne pas, vérifie ta clé API dans “Paramètres IA”

Pense à personnaliser l’icône (logo.ico) pour ton branding

Pour toute question, consulte la doc interne ou ouvre une Issue sur ton dépôt GitHub

🏆 Crédits
Développé par NovaDevSysthem & IA Studio
Interface inspirée par les meilleures pratiques dev tools 2025