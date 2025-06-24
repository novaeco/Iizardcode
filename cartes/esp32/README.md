# ESP32

L'ESP32 est un SoC Wi‑Fi/Bluetooth très populaire produit par Espressif.
Documentation officielle : <https://docs.espressif.com/projects/esp-idf/en/latest/esp32/>.

Pour flasher un firmware avec DevCenter, ouvrez l'onglet **Projet** puis
**Flash ESP32**. Le port série est détecté automatiquement grâce à la fonction
`flash_esp32()` fournie dans `project_utils.py` (le module `pyserial` est déjà
présent dans `requirements.txt`).
