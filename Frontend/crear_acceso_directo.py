import os
import sys
import winshell
from win32com.client import Dispatch

# Obtén el ejecutable de Python del entorno virtual
venv_python = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".venv", "Scripts", "python.exe"))
if not os.path.exists(venv_python):
    venv_python = sys.executable  # fallback al Python global

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))
desktop = winshell.desktop()
shortcut_path = os.path.join(desktop, "PCBuildr.lnk")
icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icono.ico"))
if not os.path.exists(icon_path):
    icon_path = venv_python

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.TargetPath = venv_python
shortcut.Arguments = f'"{script_path}"'
shortcut.WorkingDirectory = os.path.dirname(script_path)
shortcut.IconLocation = icon_path
shortcut.save()

print(f"Acceso directo creado en: {shortcut_path}")
