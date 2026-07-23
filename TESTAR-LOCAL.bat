@echo off
REM GeoRanking Presenca Digital — teste local
REM Sobe um servidor em http://127.0.0.1:8099 e abre o navegador.
REM (os componentes .dc.html carregam via fetch, por isso precisa de HTTP)
cd /d "%~dp0"
start "" "http://127.0.0.1:8099/"
echo.
echo  Servidor local em http://127.0.0.1:8099
echo  - Prototipo:        /Presenca (index redireciona sozinho)
echo  - Criador cartoes:  /Cartao de Avaliacao.dc.html
echo  - Teste da API:     /integracao.html
echo.
echo  Feche esta janela para parar o servidor.
echo.
python -m http.server 8099 --bind 127.0.0.1
