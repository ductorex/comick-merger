@echo off
REM Launch the Comick Merger GUI

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found.
    echo Please run: uv sync
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m comick_merger.main
