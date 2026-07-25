@echo off
REM Sobe o backend local da IA (proxy OpenAI). A chave fica no .env (nao vai pro git).
cd /d "%~dp0"
echo Iniciando backend da IA em http://127.0.0.1:8788 ...
python server.py
pause
