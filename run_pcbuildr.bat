@echo off
cd /d "%~dp0"
echo ====================================================
echo PCBuildr - Iniciando aplicacion
echo ====================================================
echo.
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo Iniciando Backend...
start "PCBuildr Backend" cmd /k "cd Backend && python main.py"

echo Esperando a que el backend esté listo...
timeout /t 5 /nobreak

echo.
echo Iniciando Frontend...
cd Frontend
python app.py

echo.
echo Cerrando PCBuildr...
taskkill /FI "WINDOWTITLE eq PCBuildr Backend" /T /F >nul 2>&1
echo Done!
