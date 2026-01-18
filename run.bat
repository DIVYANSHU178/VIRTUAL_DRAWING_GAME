@echo off
CALL ".\\.venv\\Scripts\\activate.bat"
pip install -r requirements.txt
python virtual_drawing.py
