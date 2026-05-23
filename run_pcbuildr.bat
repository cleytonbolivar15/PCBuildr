@echo off
REM PCBuildr Launcher for Windows
REM This batch file starts the PCBuildr application automatically

cd /d "%~dp0"
echo ====================================================
echo PCBuildr - Iniciando aplicacion
echo ====================================================
echo.

REM Check if Python venv exists
if exist .venv\Scripts\python.exe (
    echo Usando entorno virtual...
    set PYTHON=.venv\Scripts\python.exe
) else (
    echo Usando Python global...
    set PYTHON=python
)

echo.
echo Ejecutando launcher de PCBuildr...
%PYTHON% run_app.py

pause

echo.
echo Cerrando PCBuildr...
taskkill /FI "WINDOWTITLE eq PCBuildr Backend" /T /F >nul 2>&1
echo Done!
