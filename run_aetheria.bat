@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Python virtual environment not found.
    echo Please follow the setup instructions in README.txt first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m streamlit run app.py

pause