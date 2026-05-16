#!/usr/bin/env python3
"""
PCBuildr Launcher - Starts backend and frontend automatically
"""
import subprocess
import sys
import os
import time
import socket

def is_port_open(port, host="127.0.0.1"):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False

def wait_for_backend(max_attempts=30, host="127.0.0.1", port=8000):
    """Wait for backend to be ready"""
    print(f"⏳ Esperando que el backend esté listo en {host}:{port}...")
    for attempt in range(max_attempts):
        if is_port_open(port, host):
            print(f"✅ Backend está listo!")
            return True
        print(f"  Intento {attempt + 1}/{max_attempts}...")
        time.sleep(1)
    return False

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, "Backend")
    frontend_dir = os.path.join(project_root, "Frontend")
    
    print("=" * 60)
    print("PCBuildr - Iniciando servicios")
    print("=" * 60)
    
    # Activar venv si está disponible
    venv_python = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        venv_python = sys.executable
    
    # Iniciar backend en un proceso separado
    print("\n🚀 Iniciando Backend...")
    backend_cmd = [venv_python, os.path.join(backend_dir, "main.py")]
    try:
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        print(f"✅ Backend iniciado (PID: {backend_process.pid})")
    except Exception as e:
        print(f"❌ Error al iniciar backend: {e}")
        return 1
    
    # Esperar a que el backend esté listo
    if not wait_for_backend():
        print("❌ El backend no se inició correctamente")
        backend_process.terminate()
        return 1
    
    # Esperar un poco más para que el backend se estabilice
    time.sleep(2)
    
    # Iniciar frontend
    print("\n🎨 Iniciando Frontend...")
    frontend_cmd = [venv_python, os.path.join(frontend_dir, "app.py")]
    try:
        frontend_process = subprocess.run(
            frontend_cmd,
            cwd=frontend_dir
        )
    except Exception as e:
        print(f"❌ Error al iniciar frontend: {e}")
    finally:
        # Limpiar backend cuando el frontend se cierra
        print("\n🛑 Cerrando servicios...")
        backend_process.terminate()
        backend_process.wait(timeout=5)
        print("✅ Servicios detenidos")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
