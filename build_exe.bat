@echo off
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed main_gui.py
pause
