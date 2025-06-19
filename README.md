# DevCenter PRO — Qwen Edition ++

**Outil de développement tout-en-un** pour projets ESP32, BPI, automation et IA.  
Interface graphique simple, professionnelle, toutes fonctions avancées activées.

---

## Fonctionnalités principales

- Génération automatique de projet ESP32/BPI (template, src/, README.md)
- Création d’un fichier `.code-workspace` (VSCode)
- Génération auto de README.md, OpenAPI, CHANGELOG, version.txt
- Flash ESP32 (détection auto du port COM, bouton unique)
- Intégration GitHub : commit/push, gestion erreurs, ouverture dépôt d’un clic
- Gestion multi-profil utilisateur (sauvegarde/bascule, profils illimités)
- Historique IA local par projet (chaque prompt/réponse sauvegardé)
- Panneau de logs en direct (statut de chaque action, commandes exécutées)
- Assistant IA Codex/OpenAI (saisie de prompt, réponse API, sauvegarde)
- Générateur d’actions CI/CD (GitHub Actions)
- Auto-installation modules Python (requests, pyserial…)
- Build .exe universel via `build_exe.bat`
- **100% autonome, zéro config manuelle**.

---

## Prérequis

- Windows 10/11, Python 3.8+
- (Optionnel) Git, VSCode, Docker Desktop (auto-install possible)
- Clé API OpenAI (pour l’IA cloud, à insérer dans l’UI)

---

## Installation et lancement

1. **Dézippe** le dossier où tu veux.
2. **Lance `main.py`** (double-clic ou `python main.py`).
   - Ou lance `build_exe.bat` puis exécute le `.exe` généré dans `/dist`.
3. **Toutes les dépendances** s’installent automatiquement.
4. Utilise l’interface (onglets, boutons) pour chaque tâche.

---

## Utilisation

- **Onglet Projet** : génération, workspace, README, OpenAPI, CHANGELOG, flash ESP32, profils, reset git.
- **Onglet GitHub** : push, ouverture dépôt (modifie l’URL si besoin dans le code).
- **Onglet IA** : envoie ton prompt, copie/colle ta clé API, récupère la réponse, historique sauvegardé.
- **Onglet Outils avancés** : menu CI/CD, logs.

---

## Options avancées

- **Personnalisation UI** : onglets, couleurs, modernisation via ttkbootstrap ou customtkinter.
- **Ajout de composants hardware :**
   - Ajoute des callbacks pour piloter GPIO, capteurs, etc.
   - Branche des drivers LVGL, I2C, UART, etc.
   - Utilise WSL2 pour lancer des scripts Linux ou toolchains ESP32.

---

## Déploiement .EXE

- Lance `build_exe.bat` : tout est compilé, .exe prêt à l’emploi dans `/dist`.
- L’auto-install fonctionne aussi côté .exe.

---

## Support

Pour toute question, modif ou extension, contacte ton dev/mainteneur (ou l’IA du DevCenter !).

---
