@echo off
setlocal enabledelayedexpansion

REM Verifica se um comando foi fornecido
if "%~1"=="" (
    goto :show_help
)

REM Executa o comando solicitado
if /i "%~1"=="backend" (
    echo Iniciando servidor Django...
    cd backend
    python manage.py runserver
    goto :eof
)

if /i "%~1"=="frontend" (
    echo Iniciando servidor Vite...
    cd frontend
    call npm run dev
    goto :eof
)

if /i "%~1"=="install" (
    echo Instalando dependencias do backend...
    cd backend
    poetry install
    
    echo Instalando dependencias do frontend...
    cd ..\frontend
    call npm install
    goto :eof
)

if /i "%~1"=="migrate" (
    echo Executando migracoes do Django...
    cd backend
    python manage.py migrate
    goto :eof
)

if /i "%~1"=="test" (
    echo Executando testes do backend...
    cd backend
    python manage.py test
    goto :eof
)

if /i "%~1"=="help" (
    goto :show_help
)

:show_help
echo Uso: run.bat [comando]
echo.
echo Comandos disponiveis:
echo   backend     - Inicia o servidor Django
echo   frontend    - Inicia o servidor Vite
echo   install     - Instala as dependencias do backend e frontend
echo   migrate     - Executa as migracoes do Django
echo   test        - Executa os testes do backend
echo   help        - Mostra esta ajuda
exit /b 1 