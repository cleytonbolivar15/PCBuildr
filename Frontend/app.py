import sys
import requests
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QSizePolicy, QFrame,
    QLineEdit, QPushButton, QTabWidget, QApplication, QComboBox, QDockWidget,
    QListWidget, QListWidgetItem, QSplitter, QFileDialog, QInputDialog, QDesktopWidget,
    QDialog, QTextEdit, QProgressBar, QFormLayout, QMessageBox, QStackedWidget
)
from PyQt5.QtCore import Qt, QSize, QUrl, QTimer
import subprocess
import time
import socket
import os
import re
import json
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices, QColor
import random
import sqlite3
from datetime import datetime
import hashlib

# Import Bytecoon AI assistant instead of OpenAI
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ai.bytecoon import Bytecoon
bytecoon = None  # Will be initialized after language selection

def is_port_open(port, host="127.0.0.1"):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False

def is_backend_ready(port=8000, host="127.0.0.1", timeout=10):
    """Check if backend is ready"""
    for i in range(timeout):
        if is_port_open(port, host):
            return True
        time.sleep(1)
    return False

class LoadingDialog(QDialog):
    def __init__(self, mensaje="Iniciando servicios..."):
        super().__init__()
        self.setWindowTitle("PCBuildr - Cargando")
        # Ajusta tamaño y centra la ventana
        screen = QDesktopWidget().availableGeometry()
        width, height = 320, 120
        self.setFixedSize(width, height)
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - height) // 2
        )
        self.setModal(True)
        layout = QVBoxLayout()
        label = QLabel(mensaje)
        label.setStyleSheet("color: #1976D2; font-size: 18px; font-weight: bold; text-align: center;")
        layout.addWidget(label)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        layout.addWidget(self.progress)
        self.setLayout(layout)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "pcbuildr.db")

APP_STYLE_DARK = """
QWidget {
    background: #181c20;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 15px;
    color: #e3eafc;
}
QTabWidget::pane {
    border: none;
    background: #23272b;
}
QTabBar {
    background: #23272b;
    border: none;
}
QTabBar::tab {
    background: #23272b;
    border: 2px solid #1976D2;
    border-radius: 16px 16px 0 0;
    min-width: 140px;
    max-width: 220px;
    min-height: 54px;
    margin-right: 10px;
    margin-left: 10px;
    padding: 16px 18px;
    font-weight: 600;
    color: #b0bec5;
    white-space: nowrap;
    text-align: center;
}
QTabBar::tab:selected {
    background: #181c20;
    color: #00bfff;
    border-bottom: 3px solid #00bfff;
}
QTabBar::tab:hover {
    background: #22262a;
    color: #00bfff;
}
QTabBar::tab:!selected {
    margin-top: 8px;
}
QLabel {
    font-size: 20px;
    font-weight: 600;
    color: #00bfff;
    margin-bottom: 12px;
}
QPushButton {
    background: #00bfff;
    color: #181c20;
    border-radius: 28px;
    padding: 12px 24px;
    font-size: 18px;
    font-weight: 700;
    margin-left: 8px;
    margin-top: 0px;
    border: 2px solid #1976D2;
    margin-bottom: 12px;
    margin-right: 8px;
    min-width: 120px;
    max-width: 260px;
    min-height: 38px;
}
QPushButton[wide="true"] {
    min-width: 180px;
    max-width: 320px;
}
QPushButton:hover {
    background: #0099cc;
    border: 2px solid #00bfff;
}
QTextEdit, QListWidget {
    background: #23272b;
    border: 1px solid #444;
    border-radius: 14px;
    font-size: 17px;
    color: #e3eafc;
    padding: 10px;
}
QProgressBar {
    border: 1px solid #00bfff;
    border-radius: 14px;
    text-align: center;
    height: 22px;
}
QProgressBar::chunk {
    background-color: #00bfff;
    border-radius: 14px;
}
QMainWindow, QWidget, QDialog {
    border: 2px solid #000000;
    border-radius: 8px;
}
QLineEdit {
    background: #23272b;
    color: #e3eafc;
    border: 2px solid #1976D2;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 17px;
}
QLineEdit:focus {
    border: 2px solid #00bfff;
}
"""

APP_STYLE_LIGHT = """
QWidget {
    background: #d3d6db;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 15px;
    color: #23272b;
}
QTabWidget::pane {
    border: none;
    background: #e2e4e8;
}
QTabBar {
    background: #e2e4e8;
    border: none;
}
QTabBar::tab {
    background: #e2e4e8;
    border: 2px solid #b0bec5;
    border-radius: 16px 16px 0 0;
    min-width: 140px;
    max-width: 220px;
    min-height: 54px;
    margin-right: 10px;
    margin-left: 10px;
    padding: 16px 18px;
    font-weight: 600;
    color: #1976D2;
    white-space: nowrap;
    text-align: center;
}
QTabBar::tab:selected {
    background: #d3d6db;
    color: #1976D2;
    border-bottom: 3px solid #1976D2;
}
QTabBar::tab:hover {
    background: #c7c9ce;
    color: #1976D2;
}
QTabBar::tab:!selected {
    margin-top: 8px;
}
QLabel {
    font-size: 20px;
    font-weight: 600;
    color: #1976D2;
    margin-bottom: 12px;
}
QPushButton {
    background: #1976D2;
    color: #e3eafc;
    border-radius: 28px;
    padding: 12px 24px;
    font-size: 18px;
    font-weight: 700;
    margin-left: 8px;
    margin-top: 0px;
    border: 2px solid #b0bec5;
    margin-bottom: 12px;
    margin-right: 8px;
    min-width: 120px;
    max-width: 260px;
    min-height: 38px;
}
QPushButton[wide="true"] {
    min-width: 180px;
    max-width: 320px;
}
QPushButton:hover {
    background: #00bfff;
    border: 2px solid #00bfff;
    color: #181c20;
}
QTextEdit, QListWidget {
    background: #e2e4e8;
    border: 1px solid #b0bec5;
    border-radius: 14px;
    font-size: 17px;
    color: #23272b;
    padding: 10px;
}
QProgressBar {
    border: 1px solid #1976D2;
    border-radius: 14px;
    text-align: center;
    height: 22px;
}
QProgressBar::chunk {
    background-color: #1976D2;
    border-radius: 14px;
}
QMainWindow, QWidget, QDialog {
    border: 2px solid #000000;
    border-radius: 8px;
}
QLineEdit {
    background: #e2e4e8;
    color: #23272b;
    border: 2px solid #1976D2;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 17px;
}
QLineEdit:focus {
    border: 2px solid #00bfff;
}
"""

WELCOME_STYLE = """
QWidget {
    background: #181c20;
    border-radius: 18px;
}
QLabel#welcomeTitle {
    font-size: 32px;
    font-weight: bold;
    color: #00bfff;
    margin-bottom: 18px;
}
QLabel#welcomeDesc {
    font-size: 18px;
    color: #e3eafc;
    margin-bottom: 24px;
}
QPushButton#welcomeBtn {
    background: #00bfff;
    color: #181c20;
    border-radius: 18px;
    padding: 12px 36px;
    font-size: 18px;
    font-weight: 600;
    border: none;
}
QPushButton#welcomeBtn:hover {
    background: #0099cc;
}
"""

class WelcomeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido a PCBuildr")
        # Ajusta tamaño y centra la ventana
        screen = QDesktopWidget().availableGeometry()
        width, height = 500, 340
        self.setFixedSize(width, height)
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - height) // 2
        )
        self.setModal(True)
        self.setStyleSheet(WELCOME_STYLE)
        layout = QVBoxLayout()
        title = QLabel("PCBuildr 🦝")
        title.setObjectName("welcomeTitle")
        desc = QLabel(
            "PCBuildr es tu asistente inteligente para armar, comparar y mantener computadoras de escritorio.\n"
            "Te ayuda a elegir componentes compatibles, comparar precios y resolver todas tus dudas sobre hardware de PC.\n"
            "¡Empieza a crear tu próxima PC con Bytecoon, el mapache tecnológico!"
        )
        desc.setWordWrap(True)
        desc.setObjectName("welcomeDesc")
        btn = QPushButton("Empieza a crear")
        btn.setObjectName("welcomeBtn")
        btn.clicked.connect(self.accept)  # <-- Añade el evento para cerrar el diálogo
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(desc, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        self.setLayout(layout)

class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.language = "es"
        self.setWindowTitle("PCBuildr - Iniciar sesión o Registrarse")
        self.setStyleSheet("""
        QDialog {
            background: #181c20;
            border-radius: 18px;
        }
        QLabel#langLabel {
            font-size: 14px;
            color: #b0bec5;
            margin-bottom: 2px;
        }
        QPushButton[langbtn="true"] {
            font-size: 18px;
            font-weight: bold;
            min-width: 120px;
            min-height: 38px;
            background: #23272b;
            color: #00bfff;
            border-radius: 14px;
            margin-right: 8px;
            margin-left: 8px;
            border: 2px solid #1976D2;
            transition: background 0.2s;
        }
        QPushButton[langbtn="true"]:hover {
            background: #1976D2;
            color: #e3eafc;
            box-shadow: 0 2px 8px #1976D2;
        }
        QLabel#formLabel {
            font-size: 18px;
            font-weight: bold;
            color: #e3eafc;
        }
        QLineEdit {
            background: #23272b;
            color: #e3eafc;
            border: 2px solid #1976D2;
            border-radius: 10px;
            padding: 4px 10px;
            font-size: 16px;
        }
        QLineEdit:focus {
            border: 2px solid #00bfff;
        }
        QPushButton[mainbtn="true"] {
            font-size: 17px;
            font-weight: bold;
            min-width: 140px;
            min-height: 38px;
            background: #00bfff;
            color: #181c20;
            border-radius: 14px;
            margin: 8px;
            border: 2px solid #1976D2;
            box-shadow: 0 2px 8px #1976D2;
            transition: background 0.2s;
        }
        QPushButton[mainbtn="true"]:hover {
            background: #0099cc;
            color: #e3eafc;
        }
        QLabel#errorLabel {
            color: #ff6b6b;
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        }
        QLabel#demoInfo {
            background: #23272b;
            color: #00bfff;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 18px;
            margin-top: 12px;
            margin-bottom: 12px;
            font-weight: bold;
        }
        QPushButton#eyeBtn {
            background: transparent;
            border: none;
            font-size: 18px;
            min-width: 32px;
        }
        QPushButton#helpBtn {
            background: transparent;
            border: none;
            font-size: 22px;
            color: #00bfff;
            margin-left: 8px;
        }
        QLabel#logoLabel {
            margin-bottom: 8px;
        }
        """)
        # --- Layout principal ---
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # Grupo 1: Selector de idioma
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Idioma / Language:")
        lang_label.setObjectName("langLabel")
        lang_layout.addWidget(lang_label)
        self.lang_btn_es = QPushButton("Español")
        self.lang_btn_es.setProperty("langbtn", True)
        self.lang_btn_en = QPushButton("English")
        self.lang_btn_en.setProperty("langbtn", True)
        self.lang_btn_es.setCheckable(True)
        self.lang_btn_en.setCheckable(True)
        self.lang_btn_es.setChecked(True)
        self.lang_btn_es.clicked.connect(lambda: self.set_language("es"))
        self.lang_btn_en.clicked.connect(lambda: self.set_language("en"))
        lang_layout.addWidget(self.lang_btn_es)
        lang_layout.addWidget(self.lang_btn_en)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)
        # Grupo 2: Formulario usuario
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.user = QLineEdit()
        self.passw = QLineEdit()
        self.passw.setEchoMode(QLineEdit.Password)
        self.label_user = QLabel("Usuario:")
        self.label_user.setObjectName("formLabel")
        self.label_pass = QLabel("Contraseña:")
        self.label_pass.setObjectName("formLabel")
        eye_btn = QPushButton("👁️")
        eye_btn.setObjectName("eyeBtn")
        eye_btn.setCheckable(True)
        eye_btn.setToolTip("Mostrar/ocultar contraseña")
        eye_btn.clicked.connect(self.toggle_password)
        passw_hbox = QHBoxLayout()
        passw_hbox.addWidget(self.passw)
        passw_hbox.addWidget(eye_btn)
        form_layout.addRow(self.label_user, self.user)
        form_layout.addRow(self.label_pass, passw_hbox)
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)
        # Grupo 3: Info demo
        demo_info = QLabel("🔹 Ingresar como usuario demo:<br>Usuario: <b>DemoUsr</b> | Contraseña: <b>2025</b>")
        demo_info.setObjectName("demoInfo")
        demo_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.demo_info = demo_info  # <-- Añade esto para poder modificar el texto desde set_language
        main_layout.addWidget(demo_info)
        # Grupo 4: Botones de acción
        btns_hbox = QHBoxLayout()
        self.login_btn = QPushButton("Iniciar sesión")
        self.login_btn.setProperty("mainbtn", True)
        self.reg_btn = QPushButton("Registrarse")
        self.reg_btn.setProperty("mainbtn", True)
        self.del_btn = QPushButton("Borrar usuario")
        self.del_btn.setProperty("mainbtn", True)
        btns_hbox.addWidget(self.login_btn)
        btns_hbox.addWidget(self.reg_btn)
        btns_hbox.addWidget(self.del_btn)
        help_btn = QPushButton("❓")
        help_btn.setObjectName("helpBtn")
        help_btn.setToolTip("Ayuda sobre registro y recuperación de cuenta")
        help_btn.clicked.connect(self.show_help)
        btns_hbox.addWidget(help_btn)
        main_layout.addLayout(btns_hbox)
        # Feedback/Error
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.error_label)
        self.setLayout(main_layout)
        # Conexiones
        self.login_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.register)
        self.del_btn.clicked.connect(self.delete_user)
        self.is_accepted = False
        self.set_language("es")
        self.user.returnPressed.connect(self.login)
        self.passw.returnPressed.connect(self.login)

    def set_language(self, lang):
        self.language = lang
        if lang == "es":
            self.lang_btn_es.setChecked(True)
            self.lang_btn_en.setChecked(False)
            self.setWindowTitle("PCBuildr - Iniciar sesión o Registrarse")
            self.label_user.setText("Usuario:")
            self.label_pass.setText("Contraseña:")
            self.login_btn.setText("Iniciar sesión")
            self.reg_btn.setText("Registrarse")
            self.del_btn.setText("Borrar usuario")
            self.demo_info.setText("🔹 Ingresar como usuario demo:<br>Usuario: <b>DemoUsr</b> | Contraseña: <b>2025</b>")
        else:
            self.lang_btn_es.setChecked(False)
            self.lang_btn_en.setChecked(True)
            self.setWindowTitle("PCBuildr - Sign in or Register")
            self.label_user.setText("Username:")
            self.label_pass.setText("Password:")
            self.login_btn.setText("Sign in")
            self.reg_btn.setText("Register")
            self.del_btn.setText("Delete user")
            self.demo_info.setText("🔹 Demo user login:<br>Username: <b>DemoUsr</b> | Password: <b>2025</b>")
        self.error_label.setText("")

    def toggle_password(self):
        if self.passw.echoMode() == QLineEdit.Password:
            self.passw.setEchoMode(QLineEdit.Normal)
        else:
            self.passw.setEchoMode(QLineEdit.Password)

    def show_help(self):
        msg = ("¿Problemas para registrarte o recuperar tu cuenta?\n\n"
               "• Para registrarte, ingresa un usuario y contraseña y haz clic en 'Registrarse'.\n"
               "• Si olvidaste tu contraseña, crea un nuevo usuario.\n"
               "• El usuario demo siempre está disponible: Usuario: DemoUsr | Contraseña: 2025")
        if self.language == "en":
            msg = ("Problems registering or recovering your account?\n\n"
                   "• To register, enter a username and password and click 'Register'.\n"
                   "• If you forgot your password, create a new user.\n"
                   "• The demo user is always available: Username: DemoUsr | Password: 2025")
        QMessageBox.information(self, "Ayuda" if self.language == "es" else "Help", msg)

    def login(self):
        user, pw = self.user.text(), self.passw.text()
        try:
            if user.strip().lower() == "demousr":
                user = "DemoUsr"
            url = "http://127.0.0.1:8000/login"
            headers = {"Content-Type": "application/json"}
            for _ in range(5):
                try:
                    r = requests.post(url, json={"username": user, "password": pw}, headers=headers, timeout=2)
                    break
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
            else:
                self.error_label.setText("No se pudo conectar al backend. ¿Está corriendo?" if self.language == "es" else "Could not connect to backend. Is it running?")
                return
            if r.status_code == 200:
                self.is_accepted = True
                self.accept()
            elif r.status_code == 401:
                self.error_label.setText("❌ Usuario o contraseña incorrecta" if self.language == "es" else "❌ Incorrect username or password")
            elif r.status_code == 405:
                self.error_label.setText("Método no permitido. ¿Seguro que el backend está corriendo y acepta POST en /login?" if self.language == "es" else "Method not allowed. Is the backend running and accepting POST on /login?")
            elif r.status_code == 404:
                self.error_label.setText("Endpoint /login no encontrado. ¿El backend está corriendo y sin errores?" if self.language == "es" else "Endpoint /login not found. Is the backend running and error-free?")
            else:
                try:
                    msg = r.json().get("detail", "Usuario o contraseña incorrectos." if self.language == "es" else "Incorrect username or password.")
                except Exception:
                    msg = "Usuario o contraseña incorrectos." if self.language == "es" else "Incorrect username or password."
                self.error_label.setText(f"❌ {msg}")
        except Exception as e:
            self.error_label.setText(f"No se pudo conectar al servidor: {e}" if self.language == "es" else f"Could not connect to server: {e}")

    def register(self):
        user, pw = self.user.text(), self.passw.text()
        try:
            if user.strip().lower() == "demousr":
                self.error_label.setText("No puedes registrar el usuario demo." if self.language == "es" else "You cannot register the demo user.")
                return
            url = "http://127.0.0.1:8000/register"
            headers = {"Content-Type": "application/json"}
            for _ in range(5):
                try:
                    r = requests.post(url, json={"username": user, "password": pw}, headers=headers, timeout=2)
                    break
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
            else:
                self.error_label.setText("No se pudo conectar al backend. ¿Está corriendo?" if self.language == "es" else "Could not connect to backend. Is it running?")
                return
            if r.status_code == 200:
                self.error_label.setText("✅ Usuario registrado. Ahora puedes iniciar sesión." if self.language == "es" else "✅ User registered. You can now sign in.")
            elif r.status_code == 409:
                self.error_label.setText("❌ El usuario ya existe." if self.language == "es" else "❌ User already exists.")
            elif r.status_code == 405:
                self.error_label.setText("Método no permitido. ¿Seguro que el backend está corriendo y acepta POST en /register?" if self.language == "es" else "Method not allowed. Is the backend running and accepting POST on /register?")
            elif r.status_code == 404:
                self.error_label.setText("Endpoint /register no encontrado. ¿El backend está corriendo y sin errores?" if self.language == "es" else "Endpoint /register not found. Is the backend running and error-free?")
            else:
                try:
                    msg = r.json().get("detail", "Error al registrar usuario." if self.language == "es" else "Error registering user.")
                except Exception:
                    msg = "Error al registrar usuario." if self.language == "es" else "Error registering user."
                self.error_label.setText(msg)
        except Exception as e:
            self.error_label.setText(f"No se pudo conectar al servidor: {e}" if self.language == "es" else f"Could not connect to server: {e}")

    def delete_user(self):
        user = self.user.text()
        if not user:
            self.error_label.setText("Introduce el usuario a borrar." if self.language == "es" else "Enter the user to delete.")
            return
        try:
            if user.strip().lower() == "demousr":
                self.error_label.setText("No puedes borrar el usuario demo." if self.language == "es" else "You cannot delete the demo user.")
                return
            url = "http://127.0.0.1:8000/delete_user"
            headers = {"Content-Type": "application/json"}
            for _ in range(5):
                try:
                    r = requests.post(url, json={"username": user}, headers=headers, timeout=2)
                    break
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
            else:
                self.error_label.setText("No se pudo conectar al backend. ¿Está corriendo?" if self.language == "es" else "Could not connect to backend. Is it running?")
                return
            if r.status_code == 200:
                self.error_label.setText(f"✅ Usuario {user} eliminado." if self.language == "es" else f"✅ User {user} deleted.")
            elif r.status_code == 403:
                self.error_label.setText("❌ No puedes borrar el usuario demo." if self.language == "es" else "❌ You cannot delete the demo user.")
            elif r.status_code == 404:
                self.error_label.setText("Usuario no encontrado o endpoint /delete_user no existe." if self.language == "es" else "User not found or /delete_user endpoint does not exist.")
            elif r.status_code == 405:
                self.error_label.setText("Método no permitido. ¿Seguro que el backend está corriendo y acepta POST en /delete_user?" if self.language == "es" else "Method not allowed. Is the backend running and accepting POST on /delete_user?")
            else:
                try:
                    msg = r.json().get("detail", "Error al borrar usuario." if self.language == "es" else "Error deleting user.")
                except Exception:
                    msg = "Error al borrar usuario." if self.language == "es" else "Error deleting user."
                self.error_label.setText(msg)
        except Exception as e:
            self.error_label.setText(f"No se pudo conectar al servidor: {e}" if self.language == "es" else f"Could not connect to server: {e}")

class ComponentSelectorDialog(QDialog):
    def __init__(self, categoria, componentes, language="es", parent=None):
        super().__init__(parent)
        self.setWindowTitle({
            "es": f"Seleccionar {categoria}",
            "en": f"Select {categoria}"
        }[language])
        self.setModal(True)
        # Ajusta tamaño y centra la ventana
        screen = QDesktopWidget().availableGeometry()
        width, height = 700, 550
        self.setMinimumSize(width, height)
        self.resize(width, height)
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - height) // 2
        )
        layout = QVBoxLayout()

        # Filtro por tienda
        self.tienda_filter = QComboBox()
        self.tienda_filter.addItem("Todas las tiendas" if language == "es" else "All stores")
        tiendas = sorted(set(comp["tienda"] for comp in componentes))
        for t in tiendas:
            self.tienda_filter.addItem(t)
        self.tienda_filter.currentIndexChanged.connect(self.update_list)
        layout.addWidget(self.tienda_filter)

        self.list = QListWidget()
        self.componentes = componentes
        self.language = language
        self.update_list()
        layout.addWidget(self.list)

        # Imagen y link
        self.img_label = QLabel()
        self.img_label.setFixedSize(180, 180)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_label)

        self.link_btn = QPushButton("Ver producto" if language == "es" else "View product")
        self.link_btn.setEnabled(False)
        self.link_btn.clicked.connect(self.open_link)
        layout.addWidget(self.link_btn)

        self.setLayout(layout)
        self.selected = None
        self.list.itemClicked.connect(self.show_details)
        self.list.itemDoubleClicked.connect(self.select_component)
        self.current_url = ""

    def update_list(self):
        tienda = self.tienda_filter.currentText()
        self.list.clear()
        for comp in self.componentes:
            if tienda not in ("Todas las tiendas", "All stores") and comp["tienda"] != tienda:
                continue
            mano = ""
            if comp["tienda"].lower().startswith("facebook"):
                mano = " (2da mano)" if self.language == "es" else " (used)"
            item = QListWidgetItem(
                f"{comp['nombre']} - ₡{comp['precio']} - {comp['stock']}u - {comp['tienda']}{mano}"
            )
            item.setData(Qt.ItemDataRole.UserRole, comp)
            self.list.addItem(item)

    def show_details(self, item):
        comp = item.data(Qt.ItemDataRole.UserRole)
        img_url = comp.get("imagen", "")
        if img_url:
            pix = QPixmap()
            pix.loadFromData(requests.get(img_url).content)
            self.img_label.setPixmap(pix.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.img_label.clear()
        self.current_url = comp.get("url", "")
        self.link_btn.setEnabled(bool(self.current_url))

    def open_link(self):
        if self.current_url:
            QDesktopServices.openUrl(QUrl(self.current_url))

    def select_component(self, item):
        self.selected = item.data(Qt.ItemDataRole.UserRole)
        self.accept()

# --- TALLER: LÓGICA DE BASE DE DATOS Y MODELOS ---

def user_data_dir(username):
    base = os.path.join(os.path.dirname(__file__), "..", "userdata")
    if not os.path.exists(base):
        os.makedirs(base)
    # Simple hash to avoid issues with special chars in usernames
    safe_user = hashlib.sha256(username.encode("utf-8")).hexdigest()[:16]
    user_dir = os.path.join(base, safe_user)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def user_chat_path(username):
    return os.path.join(user_data_dir(username), "chat.json")

def user_builds_path(username):
    return os.path.join(user_data_dir(username), "builds.db")

def load_user_chat(username):
    path = user_chat_path(username)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_user_chat(username, chat):
    path = user_chat_path(username)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chat, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def user_db_path(username):
    # For builds/taller, use a per-user DB file
    return user_builds_path(username)

def ensure_user_db(username):
    db_path = user_db_path(username)
    if not os.path.exists(db_path):
        # Copy structure from main DB if exists, else create new
        main_db = DB_PATH
        if os.path.exists(main_db):
            import shutil
            shutil.copy(main_db, db_path)
        else:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS pcs (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    fecha_creacion TEXT,
                    estado TEXT,
                    notas_usuario TEXT
                )
            """)
            c.execute("""
//
                CREATE TABLE IF NOT EXISTS componentes (
                    id INTEGER PRIMARY KEY,
                    pc_id INTEGER,
                    tipo TEXT,
                    nombre TEXT,
                    precio REAL,
                    tienda TEXT,
                    link_producto TEXT
                )
            """)
            c.execute("""
//
                CREATE TABLE IF NOT EXISTS fallos (
                    id INTEGER PRIMARY KEY,
                    pc_id INTEGER,
                    fecha TEXT,
                    descripcion TEXT,
                    solucion TEXT
                )
            """)
            conn.commit()
            conn.close()

# Cambia las funciones de taller para aceptar username y operar sobre su DB
def taller_get_pcs(username):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("SELECT id, nombre, fecha_creacion, estado, notas_usuario FROM pcs ORDER BY fecha_creacion DESC")
    pcs = c.fetchall()
    conn.close()
    return pcs

def taller_get_pc(username, pc_id):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("SELECT id, nombre, fecha_creacion, estado, notas_usuario FROM pcs WHERE id=?", (pc_id,))
    pc = c.fetchone()
    c.execute("SELECT id, tipo, nombre, precio, tienda, link_producto FROM componentes WHERE pc_id=?", (pc_id,))
    componentes = c.fetchall()
    c.execute("SELECT id, fecha, descripcion, solucion FROM fallos WHERE pc_id=? ORDER BY fecha DESC", (pc_id,))
    fallos = c.fetchall()
    conn.close()
    return pc, componentes, fallos

def taller_add_pc(username, nombre, estado="funcional", notas_usuario=""):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO pcs (nombre, fecha_creacion, estado, notas_usuario) VALUES (?, ?, ?, ?)", (nombre, fecha, estado, notas_usuario))
    pc_id = c.lastrowid
    conn.commit()
    conn.close()
    return pc_id

def taller_update_pc(username, pc_id, nombre, estado, notas_usuario):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("UPDATE pcs SET nombre=?, estado=?, notas_usuario=? WHERE id=?", (nombre, estado, notas_usuario, pc_id))
    conn.commit()
    conn.close()

def taller_add_componente(username, pc_id, tipo, nombre, precio, tienda, link_producto):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("INSERT INTO componentes (pc_id, tipo, nombre, precio, tienda, link_producto) VALUES (?, ?, ?, ?, ?, ?)",
              (pc_id, tipo, nombre, precio, tienda, link_producto))
    conn.commit()
    conn.close()

def taller_update_componente(username, comp_id, tipo, nombre, precio, tienda, link_producto):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("UPDATE componentes SET tipo=?, nombre=?, precio=?, tienda=?, link_producto=? WHERE id=?",
              (tipo, nombre, precio, tienda, link_producto, comp_id))
    conn.commit()
    conn.close()

def taller_delete_componente(username, comp_id):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("DELETE FROM componentes WHERE id=?", (comp_id,))
    conn.commit()
    conn.close()

def taller_add_fallo(username, pc_id, descripcion, solucion=""):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO fallos (pc_id, fecha, descripcion, solucion) VALUES (?, ?, ?, ?)", (pc_id, fecha, descripcion, solucion))
    conn.commit()
    conn.close()

def taller_update_fallo(username, fallo_id, descripcion, solucion):
    ensure_user_db(username)
    conn = sqlite3.connect(user_db_path(username))
    c = conn.cursor()
    c.execute("UPDATE fallos SET descripcion=?, solucion=? WHERE id=?", (descripcion, solucion, fallo_id))
    conn.commit()
    conn.close()

def taller_export_pc_json(username, pc_id):
    pc, componentes, fallos = taller_get_pc(username, pc_id)
    data = {
        "pc": {
            "id": pc[0], "nombre": pc[1], "fecha_creacion": pc[2], "estado": pc[3], "notas_usuario": pc[4]
        },
        "componentes": [
            {"id": c[0], "tipo": c[1], "nombre": c[2], "precio": c[3], "tienda": c[4], "link_producto": c[5]}
            for c in componentes
        ],
        "fallos": [
            {"id": f[0], "fecha": f[1], "descripcion": f[2], "solucion": f[3]}
            for f in fallos
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

class RegistrarFalloDialog(QDialog):
    def __init__(self, pc_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar fallo")
        self.setModal(True)
        # Ajusta tamaño y centra la ventana
        screen = QDesktopWidget().availableGeometry()
        width = 400
        self.setMinimumWidth(width)
        self.resize(width, 300)
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - 300) // 2
        )
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Describe el fallo o síntoma:"))
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Registrar")
        self.btn_cancel = QPushButton("Cancelar")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        self.setLayout(layout)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_descripcion(self):
        return self.desc_edit.toPlainText().strip()

class EditarComponenteDialog(QDialog):
    def __init__(self, comp=None, parent=None, language="es"):
        super().__init__(parent)
        self.setWindowTitle(
            ("Editar componente" if language == "es" else "Edit component") if comp else
            ("Agregar componente" if language == "es" else "Add component")
        )
        self.setModal(True)
        # Ajusta tamaño y centra la ventana
        screen = QDesktopWidget().availableGeometry()
        width = 400
        self.setMinimumWidth(width)
        self.resize(width, 300)
        self.move(
            screen.left() + (screen.width() - width) // 2,
            screen.top() + (screen.height() - 300) // 2
        )
        layout = QFormLayout()
        self.language = language
        self.tipo_combo = QComboBox()
        self.tipo_map = {
            "Procesador": "CPU",
            "Motherboard": "Motherboard",
            "RAM": "RAM",
            "GPU": "GPU",
            "Fuente": "Fuente",
            "Gabinete": "Gabinete",
            "Ventilador": "Ventilador",
            "Almacenamiento": "Almacenamiento",
            "Otro": "Otro",
            "Processor": "CPU",
            "Motherboard": "Motherboard",
            "RAM": "RAM",
            "GPU": "GPU",
            "PSU": "Fuente",
            "Case": "Gabinete",
            "Fan": "Ventilador",
            "Storage": "Almacenamiento",
            "Other": "Otro"
        }
        tipos_es = ["Procesador", "Motherboard", "RAM", "GPU", "Fuente", "Gabinete", "Ventilador", "Almacenamiento", "Otro"]
        tipos_en = ["Processor", "Motherboard", "RAM", "GPU", "PSU", "Case", "Fan", "Storage", "Other"]
        tipos = tipos_es if language == "es" else tipos_en
        self.tipo_combo.addItems(tipos)
        # Selecciona el tipo si comp existe
        if comp:
            tipo_val = comp[1]
            for i, t in enumerate(tipos):
                if self.tipo_map.get(t, t) == tipo_val:
                    self.tipo_combo.setCurrentIndex(i)
                    break
        # --- NUEVO: Marca y Modelo en vez de Nombre ---
        self.marca = QLineEdit("")
        self.modelo = QLineEdit("")
        if comp:
            # comp[2] era "nombre", ahora intentamos separar marca y modelo si es posible
            nombre = comp[2]
            partes = nombre.split(" ", 1)
            self.marca.setText(partes[0] if len(partes) > 0 else "")
            self.modelo.setText(partes[1] if len(partes) > 1 else "")
        # --- RAM: cantidad y capacidad ---
        self.cantidad = QComboBox()
        self.cantidad.addItems([str(i) for i in range(1, 5)])
        self.capacidad = QComboBox()
        self.capacidad.addItems(["4GB", "8GB", "16GB", "32GB", "64GB"])
        if comp and self.tipo_map.get(self.tipo_combo.currentText(), "") == "RAM":
            # Intenta extraer cantidad y capacidad del modelo si es posible
            modelo = self.modelo.text()
            for cap in ["4GB", "8GB", "16GB", "32GB", "64GB"]:
                if cap.lower() in modelo.lower():
                    self.capacidad.setCurrentText(cap)
                    break
        self.precio = QLineEdit(str(comp[3]) if comp else "")
        self.tienda = QLineEdit(comp[4] if comp else "")
        self.link = QLineEdit(comp[5] if comp else "")
        layout.addRow(self.tr("Tipo:", language), self.tipo_combo)
        layout.addRow(self.tr("Marca:", language), self.marca)
        layout.addRow(self.tr("Modelo:", language), self.modelo)
        # Solo muestra cantidad/capacidad si es RAM
        self.tipo_combo.currentIndexChanged.connect(self._toggle_ram_fields)
        self.ram_fields = QWidget()
        ram_layout = QHBoxLayout()
        ram_layout.addWidget(QLabel(self.tr("Cantidad:", language)))
        ram_layout.addWidget(self.cantidad)
        ram_layout.addWidget(QLabel(self.tr("Capacidad:", language)))
        ram_layout.addWidget(self.capacidad)
        self.ram_fields.setLayout(ram_layout)
        layout.addRow(self.ram_fields)
        self._toggle_ram_fields()
        layout.addRow(self.tr("Precio:", language), self.precio)
        layout.addRow(self.tr("Tienda:", language), self.tienda)
        layout.addRow(self.tr("Link producto:", language), self.link)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton(self.tr("Guardar", language))
        self.btn_cancel = QPushButton(self.tr("Cancelar", language))
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)
        self.setLayout(layout)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def _toggle_ram_fields(self):
        tipo = self.tipo_map.get(self.tipo_combo.currentText(), "")
        self.ram_fields.setVisible(tipo == "RAM")

    def tr(self, text, lang=None):
        translations = {
            "Tipo:": "Type:",
            "Marca:": "Brand:",
            "Modelo:": "Model:",
            "Cantidad:": "Qty:",
            "Capacidad:": "Capacity:",
            "Precio:": "Price:",
            "Tienda:": "Store:",
            "Link producto:": "Product link:",
            "Guardar": "Save",
            "Cancelar": "Cancel",
        }
        if (lang or self.language) == "en":
            return translations.get(text, text)
        return text

    def get_data(self):
        tipo_text = self.tipo_combo.currentText()
        tipo = self.tipo_map.get(tipo_text, tipo_text)
        # Marca y modelo se unen para guardar como "nombre"
        nombre = f"{self.marca.text().strip()} {self.modelo.text().strip()}".strip()
        # Si es RAM, añade cantidad y capacidad al modelo
        if tipo == "RAM":
            nombre = f"{self.marca.text().strip()} {self.modelo.text().strip()} {self.cantidad.currentText()}x{self.capacidad.currentText()}"
        return (
            tipo,
            nombre,
            float(self.precio.text().strip() or 0),
            self.tienda.text().strip(),
            self.link.text().strip()
        )

class TallerTab(QWidget):
    def __init__(self, parent=None, username="DemoUsr"):
        super().__init__(parent)
        self.username = username
        self.language = getattr(parent, "language", "es") if parent else "es"
        layout = QHBoxLayout()
        self.pc_list = QListWidget()
        self.pc_list.setMinimumWidth(320)
        self.pc_list.itemClicked.connect(self.on_pc_selected)
        layout.addWidget(self.pc_list)
        self.detail_panel = QWidget()
        self.detail_layout = QVBoxLayout()
        self.detail_panel.setLayout(self.detail_layout)
        layout.addWidget(self.detail_panel)
        self.setLayout(layout)
        self.btn_nueva_pc = QPushButton(self.tr("Nueva PC"))
        self.btn_nueva_pc.clicked.connect(self.nueva_pc)
        layout.insertWidget(0, self.btn_nueva_pc)
        self.selected_pc_id = None
        self.refresh_pc_list()

    def tr(self, text):
        # Usa la función de traducción del padre si existe
        parent = self.parent()
        if parent is not None and hasattr(parent, "tr"):
            return parent.tr(text)
        return text

    def refresh_pc_list(self):
        self.pc_list.clear()
        for pc in taller_get_pcs(self.username):
            item = QListWidgetItem(f"{pc[1]} ({pc[3]})")
            item.setData(Qt.ItemDataRole.UserRole, pc[0])
            self.pc_list.addItem(item)
        for i in reversed(range(self.detail_layout.count())):
            item = self.detail_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        self.selected_pc_id = None

    def on_pc_selected(self, item):
        pc_id = item.data(Qt.ItemDataRole.UserRole)
        self.selected_pc_id = pc_id
        pc, componentes, fallos = taller_get_pc(self.username, pc_id)
        for i in reversed(range(self.detail_layout.count())):
            item = self.detail_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        self.detail_layout.addWidget(QLabel(f"<b>{self.tr('Notas:')}</b> {pc[4]}"))
        self.detail_layout.addWidget(QLabel(f"<b>{self.tr('Fecha creación:')}</b> {pc[2]}"))
        self.detail_layout.addWidget(QLabel(f"<b>{self.tr('Componentes:')}</b>"))
        for comp in componentes:
            # comp[2] ahora es "marca modelo" o "marca modelo cantidadxcapacidad" para RAM
            comp_str = f"{comp[1]}: {comp[2]} (₡{int(comp[3])}) [{comp[4]}]"
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(comp_str))
            btn_edit = QPushButton(self.tr("Editar"))
            btn_edit.setFixedWidth(80)
            btn_edit.clicked.connect(lambda _, cid=comp[0]: self.editar_componente(cid))
            btn_del = QPushButton(self.tr("Eliminar"))
            btn_del.setFixedWidth(80)
            btn_del.clicked.connect(lambda _, cid=comp[0]: self.eliminar_componente(cid))
            hbox.addWidget(btn_edit)
            hbox.addWidget(btn_del)
            container = QWidget()
            container.setLayout(hbox)
            self.detail_layout.addWidget(container)
        btn_add_comp = QPushButton(self.tr("Agregar componente"))
        btn_add_comp.clicked.connect(self.agregar_componente)
        self.detail_layout.addWidget(btn_add_comp)
        # --- Nuevo botón para detectar fallos ---
        btn_detectar_fallos = QPushButton(self.tr("Detectar fallos"))
        btn_detectar_fallos.clicked.connect(self.detectar_fallos_build)
        self.detail_layout.addWidget(btn_detectar_fallos)
        # --- Fin botón nuevo ---
        self.detail_layout.addWidget(QLabel(f"<b>{self.tr('Fallos:')}</b>"))
        for fallo in fallos:
            fallo_str = f"{fallo[1]}: {fallo[2]}"
            if fallo[3]:
                fallo_str += f"\n{self.tr('Solución:')} {fallo[3]}"
            self.detail_layout.addWidget(QLabel(fallo_str))
        btn_fallo = QPushButton(self.tr("Registrar fallo"))
        btn_fallo.clicked.connect(self.registrar_fallo)
        self.detail_layout.addWidget(btn_fallo)
        btn_export = QPushButton(self.tr("Exportar a JSON"))
        btn_export.clicked.connect(self.exportar_json)
        self.detail_layout.addWidget(btn_export)
        btn_edit_pc = QPushButton(self.tr("Editar PC"))
        btn_edit_pc.clicked.connect(self.editar_pc)
        self.detail_layout.addWidget(btn_edit_pc)
        parent = self.parent()
        if parent is not None and hasattr(parent, "bytecoon_output"):
            parent.bytecoon_output.append(  # type: ignore
                f"<b>Bytecoon 🦝:</b> {self.tr('¿Qué hay de nuevo con PC')} <b>{pc[1]}</b>? {self.tr('¿Algún cambio de componente o algún fallo reportado?')}"
            )

    def nueva_pc(self):
        nombre, ok = QInputDialog.getText(self, self.tr("Nueva PC"), self.tr("Nombre de la PC:"))
        if ok and nombre.strip():
            taller_add_pc(self.username, nombre.strip())
            self.refresh_pc_list()

    def agregar_componente(self):
        if not self.selected_pc_id:
            return
        dlg = EditarComponenteDialog(parent=self, language=self.language)
        if dlg.exec_():
            tipo, nombre, precio, tienda, link = dlg.get_data()
            # Validación de compatibilidad CPU/Motherboard
            componentes = taller_get_pc(self.username, self.selected_pc_id)[1]
            cpu = None
            mb = None
            # Busca CPU y Motherboard existentes
            for c in componentes:
                if c[1] == "CPU":
                    cpu = c
                if c[1] == "Motherboard":
                    mb = c
            # Si se está agregando una CPU o Motherboard, simula la validación
            if tipo == "CPU" and mb:
                if not self.componente_compatible(nombre, mb[2]):
                    self.mostrar_advertencia_compatibilidad()
            elif tipo == "Motherboard" and cpu:
                if not self.componente_compatible(cpu[2], nombre):
                    self.mostrar_advertencia_compatibilidad()
            taller_add_componente(self.username, self.selected_pc_id, tipo, nombre, precio, tienda, link)
            self.on_pc_selected(self.pc_list.currentItem())

    def editar_componente(self, comp_id):
        ensure_user_db(self.username)
        conn = sqlite3.connect(user_db_path(self.username))
        c = conn.cursor()
        c.execute("SELECT id, tipo, nombre, precio, tienda, link_producto FROM componentes WHERE id=?", (comp_id,))
        comp = c.fetchone()
        conn.close()
        dlg = EditarComponenteDialog(comp, parent=self, language=self.language)
        if dlg.exec_():
            tipo, nombre, precio, tienda, link = dlg.get_data()
            # Validación de compatibilidad CPU/Motherboard
            componentes = taller_get_pc(self.username, self.selected_pc_id)[1]
            cpu = None
            mb = None
            for c in componentes:
                if c[1] == "CPU":
                    cpu = c
                if c[1] == "Motherboard":
                    mb = c
            if tipo == "CPU" and mb:
                if not self.componente_compatible(nombre, mb[2]):
                    self.mostrar_advertencia_compatibilidad()
            elif tipo == "Motherboard" and cpu:
                if not self.componente_compatible(cpu[2], nombre):
                    self.mostrar_advertencia_compatibilidad()
            taller_update_componente(self.username, comp_id, tipo, nombre, precio, tienda, link)
            self.on_pc_selected(self.pc_list.currentItem())

    def componente_compatible(self, cpu_nombre, mb_nombre):
        # Simulación básica: si uno es Intel y el otro Ryzen, no son compatibles
        cpu_nombre = cpu_nombre.lower()
        mb_nombre = mb_nombre.lower()
        if ("intel" in cpu_nombre and "ryzen" in mb_nombre) or ("ryzen" in cpu_nombre and "intel" in mb_nombre):
            return False
        return True

    def mostrar_advertencia_compatibilidad(self):
        msg_es = "¡Advertencia! El procesador y la placa madre seleccionados no son compatibles (Intel vs Ryzen)."
        msg_en = "Warning! The selected processor and motherboard are not compatible (Intel vs Ryzen)."
        QMessageBox.warning(self, "Compatibilidad" if self.language == "es" else "Compatibility", msg_es if self.language == "es" else msg_en)

    def eliminar_componente(self, comp_id):
        taller_delete_componente(self.username, comp_id)
        self.on_pc_selected(self.pc_list.currentItem())

    def registrar_fallo(self):
        if not self.selected_pc_id:
            return
        dlg = RegistrarFalloDialog(self.selected_pc_id, parent=self)
        if dlg.exec_():
            desc = dlg.get_descripcion()
            if desc:
                taller_add_fallo(self.username, self.selected_pc_id, desc)
                self.on_pc_selected(self.pc_list.currentItem())

    def editar_pc(self):
        if not self.selected_pc_id:
            return
        pc, _, _ = taller_get_pc(self.username, self.selected_pc_id)
        dlg = QDialog(self)
        dlg.setWindowTitle("Editar PC")
        layout = QFormLayout()
        nombre_edit = QLineEdit(pc[1])
        estado_edit = QLineEdit(pc[3])
        notas_edit = QTextEdit(pc[4])
        layout.addRow("Nombre:", nombre_edit)
        layout.addRow("Estado:", estado_edit)
        layout.addRow("Notas:", notas_edit)
        btns = QHBoxLayout()
        btn_ok = QPushButton("Guardar")
        btn_cancel = QPushButton("Cancelar")
        btns.addWidget(btn_ok)
        btns.addWidget(btn_cancel)
        layout.addRow(btns)
        dlg.setLayout(layout)
        btn_ok.clicked.connect(dlg.accept)
        btn_cancel.clicked.connect(dlg.reject)
        if dlg.exec_():
            taller_update_pc(self.username, self.selected_pc_id, nombre_edit.text(), estado_edit.text(), notas_edit.toPlainText())
            self.refresh_pc_list()

    def exportar_json(self):
        if not self.selected_pc_id:
            return
        json_str = taller_export_pc_json(self.username, self.selected_pc_id)
        fname, _ = QFileDialog.getSaveFileName(self, "Exportar PC a JSON", f"pc_{self.selected_pc_id}.json", "JSON (*.json)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(json_str)
            QMessageBox.information(self, "Exportado", f"PC exportada a {fname}")

    def detectar_fallos_build(self):
        # Obtiene los componentes actuales de la build
        if not self.selected_pc_id:
            return
        _, componentes, _ = taller_get_pc(self.username, self.selected_pc_id)
        cpu = None
        mb = None
        ram = []
        gpu = []
        fuente = None
        for c in componentes:
            if c[1] == "CPU":
                cpu = c
            elif c[1] == "Motherboard":
                mb = c
            elif c[1] == "RAM":
                ram.append(c)
            elif c[1] == "GPU":
                gpu.append(c)
            elif c[1] == "Fuente":
                fuente = c
        problemas = []
        # Compatibilidad CPU/Motherboard
        if cpu and mb and not self.componente_compatible(cpu[2], mb[2]):
            problemas.append(self.tr("El procesador y la placa madre no son compatibles (Intel vs Ryzen)."))
        # RAM mínima
        if len(ram) == 0:
            problemas.append(self.tr("No hay memoria RAM agregada."))
        # Fuente de poder
        if not fuente:
            problemas.append(self.tr("No hay fuente de poder agregada."))
        # GPU recomendación
        if not gpu:
            problemas.append(self.tr("No hay tarjeta gráfica agregada."))
        # Mostrar resultado
        if problemas:
            QMessageBox.warning(self, self.tr("Problemas detectados"), "\n".join(problemas))
        else:
            QMessageBox.information(self, self.tr("Sin problemas"), self.tr("No se detectaron fallos en la build."))

class PCBuildSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.language = getattr(parent, "language", "es") if parent else "es"
        self.outer_layout = QVBoxLayout(self)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.inner = QWidget()
        self.layout_inner = QVBoxLayout(self.inner)
        self.title = QLabel()
        self.title.setObjectName("sectionTitle")
        self.layout_inner.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.cards = []
        self.combos = {}

        # Opciones de componentes (no traducibles, son nombres de productos)
        ram_options = [
            "Kingston Fury Beast 8GB DDR4 3200MHz - ₡16,900",
            "Kingston Fury Beast 16GB DDR4 3200MHz - ₡29,900",
            "Corsair Vengeance 16GB DDR4 3200MHz - ₡32,900",
            "Corsair Vengeance 32GB DDR4 3200MHz - ₡62,900",
            "Kingston Fury Beast 32GB DDR5 5600MHz - ₡69,900",
            "Corsair Vengeance 32GB DDR5 5600MHz - ₡74,900",
            "Kingston Fury Beast 64GB DDR5 6000MHz - ₡139,900",
            "Corsair Vengeance 64GB DDR5 6000MHz - ₡149,900",
            "ADATA XPG 16GB DDR4 3200MHz - ₡28,900",
            "ADATA XPG 32GB DDR4 3200MHz - ₡59,900",
            "ADATA XPG 32GB DDR5 5600MHz - ₡68,900",
        ]
        fuente_options = [
            "Corsair CV550 550W 80+ Bronze - ₡32,900",
            "Corsair CV650 650W 80+ Bronze - ₡39,900",
            "Corsair RM750 750W 80+ Gold Modular - ₡74,900",
            "EVGA 600W 80+ White - ₡29,900",
            "EVGA 700W 80+ Bronze - ₡44,900",
            "Cooler Master MWE 650W 80+ Bronze - ₡36,900",
            "Cooler Master MWE 750W 80+ Gold Modular - ₡79,900",
            "Gigabyte P650B 650W 80+ Bronze - ₡35,900",
            "Gigabyte GP-P850GM 850W 80+ Gold Modular - ₡99,900",
        ]
        placa_options = [
            "MSI B450M-A PRO MAX AM4 - ₡54,900",
            "MSI B550M PRO-VDH WIFI AM4 - ₡69,900",
            "ASUS PRIME B550M-A WIFI AM4 - ₡74,900",
            "ASUS TUF GAMING Z690-PLUS WIFI D4 LGA1700 - ₡159,900",
            "MSI PRO Z690-A DDR4 LGA1700 - ₡139,900",
            "ASUS PRIME X570-P AM4 - ₡129,900",
            "Gigabyte B550M DS3H AM4 - ₡62,900",
            "Gigabyte Z690 UD DDR4 LGA1700 - ₡129,900",
            "ASRock B450M Steel Legend AM4 - ₡69,900",
        ]
        cpu_options = [
            "Intel Core i5-12400F 6-Core 4.4GHz LGA1700 - ₡99,900",
            "Intel Core i7-13700K 16-Core 5.4GHz LGA1700 - ₡239,900",
            "Intel Core i9-13900K 24-Core 5.8GHz LGA1700 - ₡349,900",
            "AMD Ryzen 5 5600X 6-Core 4.6GHz AM4 - ₡109,900",
            "AMD Ryzen 7 5800X 8-Core 4.7GHz AM4 - ₡159,900",
            "AMD Ryzen 9 5900X 12-Core 4.8GHz AM4 - ₡239,900",
            "AMD Ryzen 7 7700X 8-Core 5.4GHz AM5 - ₡199,900",
            "AMD Ryzen 9 7900X 12-Core 5.6GHz AM5 - ₡299,900",
            "Intel Core i3-12100F 4-Core 4.3GHz LGA1700 - ₡69,900",
        ]
        gpu_options = [
            "NVIDIA GeForce GTX 1660 Super 6GB - ₡169,900",
            "NVIDIA GeForce RTX 3060 12GB - ₡239,900",
            "NVIDIA GeForce RTX 4060 8GB - ₡259,900",
            "NVIDIA GeForce RTX 4070 12GB - ₡399,900",
            "AMD Radeon RX 6700XT 12GB - ₡299,900",
            "AMD Radeon RX 6600 8GB - ₡189,900",
            "AMD Radeon RX 6800XT 16GB - ₡449,900",
            "NVIDIA GeForce RTX 3050 8GB - ₡179,900",
            "NVIDIA GeForce RTX 4080 16GB - ₡699,900",
        ]
        almacenamiento_options = [
            "Kingston NV2 500GB M.2 NVMe SSD - ₡22,900",
            "Kingston NV2 1TB M.2 NVMe SSD - ₡39,900",
            "Kingston A400 240GB SATA SSD - ₡15,900",
            "Kingston A400 480GB SATA SSD - ₡26,900",
            "Samsung 870 EVO 1TB SATA SSD - ₡49,900",
            "Samsung 980 1TB M.2 NVMe SSD - ₡59,900",
            "WD Blue 1TB HDD 7200rpm - ₡24,900",
            "WD Blue 2TB HDD 7200rpm - ₡39,900",
            "Seagate Barracuda 2TB HDD 7200rpm - ₡38,900",
            "Crucial P3 1TB M.2 NVMe SSD - ₡37,900",
            "Crucial MX500 1TB SATA SSD - ₡47,900",
        ]
        cases_options = [
            "Corsair Crystal 280X Micro-ATX - ₡79,900",
            "Corsair Crystal 680X ATX - ₡129,900",
            "Hyte Y70 Touch ATX Panoramic - ₡159,900",
            "NZXT H510 Mid Tower ATX - ₡59,900",
            "Cooler Master NR200P Mini-ITX - ₡69,900",
            "Lian Li Lancool II Mesh ATX - ₡74,900",
            "Fractal Design Meshify C ATX - ₡84,900",
        ]
        cooler_options = [
            "Cooler Master MasterLiquid 240 AIO - ₡85,000",
            "Noctua NH-D15 Air Cooler - ₡110,000",
            "Deepcool AK620 Air Cooler - ₡70,000",
            "Arctic Liquid Freezer II 280 AIO - ₡100,000",
            "Lian Li Galahad 240 AIO - ₡110,000",
            "ROG Ryujin II 360 AIO LCD - ₡280,000",
            "Corsair H150i Elite Capellix XT AIO - ₡220,000",
        ]

        self.componentes_data = [
            ("RAM", ram_options),
            ("Fuente de poder", fuente_options),
            ("Placa madre", placa_options),
            ("Procesador", cpu_options),
            ("Tarjeta de video", gpu_options),
            ("Almacenamiento", almacenamiento_options),
            ("Gabinete", cases_options),
            ("Enfriamiento", cooler_options),
        ]
        self.labels = {}
        self.combos = {}
        for nombre, opciones in self.componentes_data:
            card = QFrame()
            card.setProperty("card", True)
            card_layout = QVBoxLayout(card)
            label = QLabel()
            label.setProperty("compLabel", True)
            self.labels[nombre] = label
            combo = QComboBox()
            combo.addItems(opciones)
            self.combos[nombre] = combo
            card_layout.addWidget(label)
            card_layout.addWidget(combo)
            card.setMinimumHeight(110)
            self.layout_inner.addWidget(card)
            self.cards.append(card)
            combo.currentIndexChanged.connect(self.update_total)

        self.total_label = QLabel("")
        self.total_label.setObjectName("totalLabel")
        self.layout_inner.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_inner.addStretch()
        self.update_total()
        scroll.setWidget(self.inner)
        self.outer_layout.addWidget(scroll)

        save_panel = QHBoxLayout()
        self.pc_name_input = QLineEdit()
        self.pc_name_input.setPlaceholderText("Nombre de la PC" if self.language == "es" else "PC Name")
        self.btn_save_pc = QPushButton("Guardar PC" if self.language == "es" else "Save PC")
        self.btn_save_pc.setStyleSheet("font-size: 16px; min-width: 120px;")
        self.btn_save_pc.clicked.connect(self.save_current_pc)
        save_panel.addWidget(self.pc_name_input)
        save_panel.addWidget(self.btn_save_pc)
        self.outer_layout.addLayout(save_panel)

        self.saved_pcs_area = QScrollArea(self)
        self.saved_pcs_area.setWidgetResizable(True)
        self.saved_pcs_area.setFixedHeight(220)
        self.saved_pcs_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #1976D2;
                border-radius: 10px;
                background: #23272b;
                margin-top: 8px;
            }
        """)
        self.saved_pcs_widget = QWidget()
        self.saved_pcs_layout = QVBoxLayout(self.saved_pcs_widget)
        self.saved_pcs_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.saved_pcs_area.setWidget(self.saved_pcs_widget)
        self.saved_pcs_label = QLabel("PCs guardadas" if self.language == "es" else "Saved PCs")
        self.outer_layout.addWidget(self.saved_pcs_label)
        self.outer_layout.addWidget(self.saved_pcs_area)

        self.saved_pcs = []

        # Consejos traducibles
        self.tips_dict = {
            "es": [
                "Verifique cuello de botella.",
                "Verifique compatibilidad entre sockets de procesador y motherboard.",
                "Verifique que la fuente de poder sea suficiente para los componentes seleccionados.",
                "Verifique tener almacenamiento y RAM suficiente para sus necesidades.",
                "Verifique que el cooler sea suficiente para el procesador."
            ],
            "en": [
                "Check for bottlenecks.",
                "Check CPU and motherboard socket compatibility.",
                "Ensure the power supply is sufficient for selected components.",
                "Ensure you have enough storage and RAM for your needs.",
                "Ensure the cooler is adequate for the processor."
            ]
        }

        self.set_language(self.language)

    def update_total(self):
        total = 0
        for combo in self.combos.values():
            text = combo.currentText()
            match = re.search(r"₡([\d,]+)", text)
            if match:
                price = int(match.group(1).replace(",", ""))
                total += price
        lang = getattr(self, "language", "es")
        label = "Estimated total: ₡{total:,}" if lang == "en" else "Total estimado: ₡{total:,}"
        self.total_label.setText(label.format(total=total))

    def save_current_pc(self):
        name = self.pc_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, self.tr("name_required"), self.tr("enter_pc_name"))
            return
        components = {}
        for nombre in self.combos:
            components[nombre] = self.combos[nombre].currentText()
        total = 0
        for c in components.values():
            match = re.search(r"₡([\d,]+)", c)
            if match:
                total += int(match.group(1).replace(",", ""))
        # Añade consejos según idioma actual
        tips = self.tips_dict.get(self.language, self.tips_dict["es"])
        self.saved_pcs.append({
            "name": name,
            "components": components,
            "total": total,
            "tips": tips
        })
        self.pc_name_input.clear()
        self.refresh_saved_pcs()

    def refresh_saved_pcs(self):
        for i in reversed(range(self.saved_pcs_layout.count())):
            item = self.saved_pcs_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        if not self.saved_pcs:
            empty = QLabel(self.tr("no_saved_pcs"))
            empty.setStyleSheet("color: #b0bec5; font-style: italic;")
            self.saved_pcs_layout.addWidget(empty)
            return
        for pc in self.saved_pcs:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background: #181c20;
                    border-radius: 8px;
                    margin-bottom: 8px;
                }
            """)
            vbox = QVBoxLayout(frame)
            title = QLabel(f"<b>{pc['name']}</b> - ₡{pc['total']:,}")
            title.setStyleSheet("font-size: 17px; color: #00bfff;")
            vbox.addWidget(title)
            for k, v in pc["components"].items():
                comp_label = QLabel(f"{k}: {v}")
                comp_label.setStyleSheet("font-size: 15px; color: #e3eafc;")
                vbox.addWidget(comp_label)
            # Consejos
            tips_box = QFrame()
            tips_box.setStyleSheet("background: #23272b; border-radius: 6px; margin-top: 6px;")
            tips_layout = QVBoxLayout(tips_box)
            tips_label = QLabel(self.tr("tips_title"))
            tips_label.setStyleSheet("font-size: 15px; color: #00bfff; margin-bottom: 2px;")
            tips_layout.addWidget(tips_label)
            for tip in pc["tips"]:
                tip_label = QLabel("• " + tip)
                tip_label.setStyleSheet("font-size: 14px; color: #b0bec5;")
                tips_layout.addWidget(tip_label)
            vbox.addWidget(tips_box)
            self.saved_pcs_layout.addWidget(frame)

    def set_language(self, lang):
        self.language = lang
        labels_es = [
            "RAM", "Fuente de poder", "Placa madre", "Procesador",
            "Tarjeta de video", "Almacenamiento", "Gabinete", "Enfriamiento"
        ]
        labels_en = [
            "RAM", "Power Supply", "Motherboard", "Processor",
            "Graphics Card", "Storage", "Case", "Cooling"
        ]
        labels = labels_es if lang == "es" else labels_en
        for i, nombre in enumerate(self.labels):
            self.labels[nombre].setText(labels[i])
        self.title.setText(self.tr("pc_build_title"))
        self.update_total()
        if hasattr(self, "pc_name_input"):
            self.pc_name_input.setPlaceholderText(self.tr("pc_name_placeholder"))
        if hasattr(self, "btn_save_pc"):
            self.btn_save_pc.setText(self.tr("save_pc_btn"))
        if hasattr(self, "saved_pcs_label"):
            self.saved_pcs_label.setText(self.tr("saved_pcs_label"))
        # Actualiza los consejos de todas las PCs guardadas
        tips = self.tips_dict.get(lang, self.tips_dict["es"])
        for pc in self.saved_pcs:
            pc["tips"] = tips
        self.refresh_saved_pcs()

    def tr(self, key):
        translations = {
            "pc_build_title": {"es": "Armado de PC", "en": "PC Build"},
            "pc_name_placeholder": {"es": "Nombre de la PC", "en": "PC Name"},
            "save_pc_btn": {"es": "Guardar PC", "en": "Save PC"},
            "saved_pcs_label": {"es": "PCs guardadas", "en": "Saved PCs"},
            "no_saved_pcs": {"es": "No hay PCs guardadas.", "en": "No saved PCs."},
            "name_required": {"es": "Nombre requerido", "en": "Name required"},
            "enter_pc_name": {"es": "Por favor ingresa un nombre para la PC.", "en": "Please enter a name for the PC."},
            "tips_title": {"es": "Consejos para tu build:", "en": "Build tips:"},
        }
        return translations.get(key, {}).get(self.language, key)

class PCBuildrApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.language = "es"
        self.theme = "dark"
        self.chat_history = []  # [(rol, mensaje)], rol: "usuario" o "asistente"
        self.setWindowTitle("PCBuildr - Tu asistente de hardware")
        self.setStyleSheet(APP_STYLE_DARK)
        main_layout = QVBoxLayout(self)
        self.sidebar_visible = False
        self.sidebar_width = 250
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        # Título
        title_layout = QHBoxLayout()
        title_label = QLabel("PCBuildr - Tu asistente de hardware")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00bfff;")
        self.title_label = title_label  # <-- Asegura que esté accesible para set_language
        title_layout.addWidget(title_label)
        self.menu_btn = QPushButton("☰")
        self.menu_btn.setFixedSize(40, 40)
        self.menu_btn.setStyleSheet("font-size: 18px; background: transparent; border: none; color: #00bfff;")
        title_layout.addWidget(self.menu_btn, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(title_layout)

        # --- Barra de navegación horizontal ---
        nav_bar = QFrame(self)
        nav_bar.setStyleSheet("""
            QFrame {
                background: #23272b;
                border: none;
                border-bottom: 2px solid #000000;
            }
            QPushButton {
                background: #23272b;
                color: #00bfff;
                border: none;
                padding: 12px 24px;
                font-size: 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #181c20;
            }
        """)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        self.btn_chat = QPushButton("Chat")
        self.btn_pcbuild = QPushButton("Armado de PC")
        self.btn_config = QPushButton("Configuración")
        self.btn_logout = QPushButton("Cerrar sesión")
        self.btn_logout.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        nav_layout.addWidget(self.btn_chat)
        nav_layout.addWidget(self.btn_pcbuild)
        nav_layout.addWidget(self.btn_config)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_logout)



        main_layout.addWidget(nav_bar)
        # --- FIN barra horizontal ---

        # Contenedor principal (donde se cambiará entre chat y armado de PC)
        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.stacked_widget)

        # --- Sección de chat ---
        self.chat_section = QWidget()
        self.stacked_widget.addWidget(self.chat_section)
        chat_layout = QVBoxLayout(self.chat_section)
        # Título
        title_chat = QLabel("Bytecoon, tu asistente IA 🦝💬")
        title_chat.setStyleSheet("font-size: 22px; font-weight: bold; color: #00bfff;")
        self.title_chat = title_chat
        chat_layout.addWidget(title_chat, alignment=Qt.AlignmentFlag.AlignHCenter)
        # Botón para reiniciar conversación (solo una vez)
        self.btn_nuevo_chat = QPushButton("Nuevo chat" if self.language == "es" else "New chat")
        self.btn_nuevo_chat.setStyleSheet("font-size: 16px; min-width: 120px;")
        self.btn_nuevo_chat.clicked.connect(self.reiniciar_chat)
        chat_layout.addWidget(self.btn_nuevo_chat, alignment=Qt.AlignmentFlag.AlignRight)
        # Área de texto (chat)
        self.bytecoon_output = QTextEdit()
        self.bytecoon_output.setReadOnly(True)
        self.bytecoon_output.setStyleSheet("""
            QTextEdit {
                background: #181c20;
                color: #e3eafc;
                border: 2px solid #1976D2;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
            }
        """)
        chat_layout.addWidget(self.bytecoon_output)
        # Entrada de texto y botón enviar
        self.bytecoon_input = QLineEdit()
        self.bytecoon_input.setPlaceholderText("Escribe tu pregunta o mensaje para Bytecoon...")
        self.bytecoon_input.setStyleSheet("""
            QLineEdit {
                background: #23272b;
                color: #e3eafc;
                border: 2px solid #1976D2;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #00bfff;
            }
        """)
        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.setStyleSheet("font-size: 16px;")
        btns_layout = QHBoxLayout()
        btns_layout.addWidget(self.bytecoon_input)
        btns_layout.addWidget(self.btn_enviar)
        chat_layout.addLayout(btns_layout)

        # --- Sección de armado de PC (PCBuildSection) ---
        self.pc_build_section = PCBuildSection(self)
        self.stacked_widget.addWidget(self.pc_build_section)
        # --- Sección de configuración (settings) ---
        self.config_section = QWidget()
        config_layout = QVBoxLayout(self.config_section)
        config_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.btn_lang = QPushButton("Cambiar a inglés" if self.language == "es" else "Switch to Spanish")
        self.btn_lang.setStyleSheet("font-size: 18px; min-width: 180px;")
        self.btn_lang.clicked.connect(self.toggle_language)
        self.btn_theme = QPushButton("Modo claro" if self.theme == "dark" else "Modo oscuro")
        self.btn_theme.setStyleSheet("font-size: 18px; min-width: 180px;")
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.btn_exit = QPushButton("Salir de la aplicación" if self.language == "es" else "Exit application")
        self.btn_exit.setStyleSheet("font-size: 18px; min-width: 180px; color: #ff6b6b; font-weight: bold;")
        self.btn_exit.clicked.connect(self.salir_app)
        config_layout.addWidget(self.btn_lang)
        config_layout.addWidget(self.btn_theme)
        config_layout.addSpacing(24)
        config_layout.addWidget(self.btn_exit)
        config_layout.addStretch()
        self.stacked_widget.addWidget(self.config_section)

        # Conexiones
        self.btn_enviar.clicked.connect(self.enviar_pregunta_bytecoon)
        self.bytecoon_input.returnPressed.connect(self.enviar_pregunta_bytecoon)
        self.btn_chat.clicked.connect(lambda: self.cambiar_seccion("chat"))
        self.btn_pcbuild.clicked.connect(lambda: self.cambiar_seccion("pcbuild"))
        self.btn_config.clicked.connect(self.abrir_configuracion)
        self.btn_logout.clicked.connect(self.cerrar_sesion)

        self.cambiar_seccion("chat")

    def set_language(self, lang):
        self.language = lang
        texts = {
            "es": {
                "title": "PCBuildr - Tu asistente de hardware",
                "chat": "Chat",
                "pcbuild": "Armado de PC",
                "config": "Configuración",
                "logout": "Cerrar sesión",
                "lang": "Cambiar a inglés",
                "theme_dark": "Modo claro",
                "theme_light": "Modo oscuro",
                "exit": "Salir de la aplicación",
                "chat_title": "Bytecoon, tu asistente IA 🦝💬",
                "input_placeholder": "Escribe tu pregunta o mensaje para Bytecoon...",
                "send": "Enviar",
                "new_chat": "Nuevo chat"
            },
            "en": {
                "title": "PCBuildr - Your hardware assistant",
                "chat": "Chat",
                "pcbuild": "PC Build",
                "config": "Settings",
                "logout": "Log out",
                "lang": "Switch to Spanish",
                "theme_dark": "Light mode",
                "theme_light": "Dark mode",
                "exit": "Exit application",
                "chat_title": "Bytecoon, your AI assistant 🦝💬",
                "input_placeholder": "Type your question or message for Bytecoon...",
                "send": "Send",
                "new_chat": "New chat"
            }
        }
        t = texts[lang]
        if hasattr(self, "title_label"):
            self.title_label.setText(t["title"])
        if hasattr(self, "btn_chat"):
            self.btn_chat.setText(t["chat"])
        if hasattr(self, "btn_pcbuild"):
            self.btn_pcbuild.setText(t["pcbuild"])
        if hasattr(self, "btn_config"):
            self.btn_config.setText(t["config"])
        if hasattr(self, "btn_logout"):
            self.btn_logout.setText(t["logout"])
        if hasattr(self, "btn_lang"):
            self.btn_lang.setText(t["lang"])
        if hasattr(self, "btn_theme"):
            self.btn_theme.setText(t["theme_dark"] if self.theme == "dark" else t["theme_light"])
        if hasattr(self, "btn_exit"):
            self.btn_exit.setText(t["exit"])
        if hasattr(self, "title_chat"):
            self.title_chat.setText(t["chat_title"])
        if hasattr(self, "bytecoon_input"):
            self.bytecoon_input.setPlaceholderText(t["input_placeholder"])
        if hasattr(self, "btn_enviar"):
            self.btn_enviar.setText(t["send"])
        if hasattr(self, "btn_nuevo_chat"):
            self.btn_nuevo_chat.setText(t["new_chat"])
        if hasattr(self, "pc_build_section"):
            self.pc_build_section.set_language(lang)
        if hasattr(self, "config_section"):
            layout = self.config_section.layout()
            if layout is not None:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item is not None:
                        w = item.widget()
                        if isinstance(w, QPushButton):
                            if w == self.btn_lang:
                                w.setText(t["lang"])
                            elif w == self.btn_theme:
                                w.setText(t["theme_dark"] if self.theme == "dark" else t["theme_light"])
                            elif w == self.btn_exit:
                                w.setText(t["exit"])
        self.setWindowTitle(t["title"])

    def enviar_pregunta_bytecoon(self):
        pregunta = self.bytecoon_input.text().strip()
        if not pregunta:
            return
        # Añadir mensaje del usuario al historial de sesión
        self.chat_history.append(("usuario", pregunta))
        if self.language == "es":
            self.bytecoon_output.append(f"<b>Tú:</b> {pregunta}")
        else:
            self.bytecoon_output.append(f"<b>You:</b> {pregunta}")
        self.bytecoon_input.clear()
        # Construir historial para el modelo
        system_prompts = {
            "es": (
                "Eres Bytecoon, un asistente experto en hardware de computadoras, PC building y soporte técnico. "
                "Responde SIEMPRE en español, de forma clara y útil. "
                "Si el usuario te pregunta por recomendaciones de componentes, "
                "da la respuesta en español y nunca mezcles inglés y español."
            ),
            "en": (
                "You are Bytecoon, an expert assistant in computer hardware, PC building, and tech support. "
                "Always reply in English, clearly and helpfully. "
                "If the user asks for component recommendations, answer in English and never mix Spanish and English."
            )
        }
        system_prompt = system_prompts.get(self.language, system_prompts["es"])
        messages = [{"role": "system", "content": system_prompt}]
        for rol, msg in self.chat_history:
            if rol == "usuario":
                messages.append({"role": "user", "content": msg})
            else:
                messages.append({"role": "assistant", "content": msg})
        try:
            # Use Bytecoon AI assistant (works offline by default)
            if bytecoon is not None:
                respuesta = bytecoon.ask(pregunta)
            else:
                respuesta = "Bytecoon not initialized" if self.language == "en" else "Bytecoon no está inicializado"
        except Exception as e:
            if self.language == "es":
                respuesta = f"Error al contactar a Bytecoon: {e}"
            else:
                respuesta = f"Error contacting Bytecoon: {e}"
        # Añadir respuesta de Bytecoon al historial antes de mostrarla
        self.chat_history.append(("asistente", respuesta))
        self.recibir_respuesta_bytecoon(respuesta)

    def reiniciar_chat(self):
        self.chat_history = []
        self.bytecoon_output.clear()
        if self.language == "es":
            self.bytecoon_output.append("<b>Bytecoon:</b> ¡Hola! ¿En qué puedo ayudarte hoy?")
        else:
            self.bytecoon_output.append("<b>Bytecoon:</b> Hi! How can I help you today?")

    def toggle_language(self):
        # Cambia el idioma de la interfaz
        new_lang = "en" if self.language == "es" else "es"
        self.set_language(new_lang)

    def toggle_theme(self):
        # Cambia el tema de la interfaz
        if self.theme == "dark":
            self.theme = "light"
            self.setStyleSheet(APP_STYLE_LIGHT)
            if hasattr(self, "btn_theme"):
                self.btn_theme.setText("Modo oscuro" if self.language == "es" else "Dark mode")
        else:
            self.theme = "dark"
            self.setStyleSheet(APP_STYLE_DARK)
            if hasattr(self, "btn_theme"):
                self.btn_theme.setText("Modo claro" if self.language == "es" else "Light mode")

    def abrir_configuracion(self):
        self.cambiar_seccion("config")

    def salir_app(self):
        QApplication.quit()

    def cerrar_sesion(self):
        # Cierra la ventana principal y vuelve a mostrar el login
        self.hide()
        auth = AuthDialog()
        if auth.exec_():
            self.set_language(auth.language)
            self.show()
        else:
            QApplication.quit()

    def cambiar_seccion(self, seccion):
        # Cambia la vista principal según la sección seleccionada
        if seccion == "chat":
            self.stacked_widget.setCurrentWidget(self.chat_section)
        elif seccion == "pcbuild":
            self.stacked_widget.setCurrentWidget(self.pc_build_section)
        elif seccion == "config":
            self.stacked_widget.setCurrentWidget(self.config_section)
        # Puedes agregar más secciones aquí si las necesitas

    def recibir_respuesta_bytecoon(self, respuesta):
        # Muestra la respuesta de Bytecoon en el chat
        self.bytecoon_output.append(f"<b>Bytecoon:</b> {respuesta}")

if __name__ == '__main__':
    # No need to wait for LM Studio - Bytecoon works offline!
    app = QApplication(sys.argv)
    welcome = WelcomeDialog()
    welcome.exec_()
    auth = AuthDialog()
    if not auth.exec_():
        sys.exit(0)

    # Initialize Bytecoon with selected language
    language = auth.language
    username = auth.user.text() or "DemoUsr"
    bytecoon = Bytecoon(language)

    mainWin = PCBuildrApp()
    mainWin.set_language(language)
    mainWin.show()
    sys.exit(app.exec_())