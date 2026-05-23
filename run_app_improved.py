#!/usr/bin/env python3
"""
PCBuildr Launcher - Automatically starts backend and frontend
This is the EASIEST way to run PCBuildr - just execute this file!
"""
import subprocess
import sys
import os
import time
import socket
import threading

def is_port_open(port, host="127.0.0.1", timeout=1):
    """Check if port is open"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def wait_for_backend(max_attempts=30, host="127.0.0.1", port=8000):
    """Wait for backend to be ready"""
    print(f"\n⏳ Esperando que el backend esté listo en {host}:{port}...")
    for attempt in range(max_attempts):
        if is_port_open(port, host):
            print(f"✅ Backend está listo en intento {attempt + 1}")
            return True
        print(f"  Intento {attempt + 1}/{max_attempts}... esperando", end='\r')
        time.sleep(1)
    return False

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, "Backend")
    frontend_dir = os.path.join(project_root, "Frontend")
    
    print("=" * 70)
    print("PCBuildr - Iniciador Automático 🦝")
    print("=" * 70)
    
    # Detectar Python executable
    venv_python = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        venv_python = sys.executable
        print(f"⚠️  Usando Python global: {venv_python}")
    else:
        print(f"✅ Usando Python del venv: {venv_python}")
    
    backend_process = None
    
    try:
        # Check if port is already in use (backend might be running)
        if is_port_open(8000):
            print("✅ Backend ya está corriendo en puerto 8000")
        else:
            print("\n🚀 Iniciando Backend...")
            backend_cmd = [venv_python, os.path.join(backend_dir, "main.py")]
            
            # Use CREATE_NEW_CONSOLE on Windows to open backend in separate window
            if sys.platform == "win32":
                backend_process = subprocess.Popen(
                    backend_cmd,
                    cwd=backend_dir,
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✅ Backend iniciado en nueva ventana (PID: {backend_process.pid})")
            else:
                backend_process = subprocess.Popen(
                    backend_cmd,
                    cwd=backend_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✅ Backend iniciado (PID: {backend_process.pid})")
            
            # Wait for backend to be ready
            if not wait_for_backend():
                print("❌ El backend no se inició correctamente después de 30 intentos")
                if backend_process:
                    backend_process.terminate()
                return 1
            
            # Extra wait for stability
            time.sleep(2)
        
        # Start frontend
        print("\n🎨 Iniciando Frontend...")
        frontend_cmd = [venv_python, os.path.join(frontend_dir, "app.py")]
        frontend_process = subprocess.run(frontend_cmd, cwd=frontend_dir)
        
        print("\n✅ Aplicación cerrada")
        return frontend_process.returncode
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupción del usuario - cerrando servicios...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    finally:
        # Cleanup backend if we started it
        if backend_process:
            try:
                print("🛑 Deteniendo Backend...")
                backend_process.terminate()
                backend_process.wait(timeout=5)
                print("✅ Backend detenido")
            except:
                backend_process.kill()
                print("✅ Backend forzadamente detenido")

if __name__ == "__main__":
    sys.exit(main())
