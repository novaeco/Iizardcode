# DevCenter PRO – Qwen Edition ++

**Outil complet tout-en-un pour projets ESP32, BPI, automation & IA.**

---

## Fonctionnalités principales

- Génération automatique de projet ESP32/BPI (template)
- Création fichier `.code-workspace` (VSCode)
- Génération README.md, OpenAPI, CHANGELOG, version.txt
- Flash ESP32 (détection auto port COM)
- Intégration GitHub (push, gestion erreurs, bouton ouvrir dépôt)
- Gestion multi-profil (sauvegarde/bascule)
- Historique IA local par projet
- Panneau de logs en direct
- Assistant IA Codex/OpenAI : prompt + réponse réelle via API, historique sauvegardé
- Générateur Actions CI/CD GitHub
- Auto-installation des modules Python (requests, pyserial…)
- Build .exe via `build_exe.bat`
- Interface claire, moderne et évolutive

---

## Prérequis

- Windows 10/11, Python 3.8+
- (Optionnel) Git, VSCode, Docker Desktop (auto-install possible)
- Clé API OpenAI (pour l’IA cloud, à insérer dans l’UI)

---

## Utilisation

1. **Dézippe** le dossier.
2. **Lance `main.py`** (double-clic ou `python main.py`).
   - Ou build `.exe` via `build_exe.bat` puis exécute dans `/dist`.
3. **Saisis ta clé OpenAI** dans l’onglet IA pour profiter de l’assistant.
4. Utilise chaque bouton selon tes besoins.

---

## Personnalisation/Extensions

- Tu peux moderniser l’UI avec [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) ou [customtkinter](https://github.com/TomSchimansky/CustomTkinter).
- Les fonctions hardware/LVGL sont branchables en python ou via port série.

---

## Support

Besoin d’aide ? Contacte ton développeur ou l’assistant IA intégré !
