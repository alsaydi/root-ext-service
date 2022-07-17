@echo off

SET FLASK_APP=main.py

.\.pyenv\Scripts\activate.bat
flask run
