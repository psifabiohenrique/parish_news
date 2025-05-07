#!/bin/bash

# Função para mostrar ajuda
show_help() {
    echo "Uso: ./run.sh [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  backend     - Inicia o servidor Django"
    echo "  frontend    - Inicia o servidor Vite"
    echo "  install     - Instala as dependências do backend e frontend"
    echo "  migrate     - Executa as migrações do Django"
    echo "  test        - Executa os testes do backend"
    echo "  help        - Mostra esta ajuda"
}

# Verifica se o comando foi fornecido
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

# Executa o comando solicitado
case $1 in
    "backend")
        echo "Iniciando servidor Django..."
        cd backend
        python manage.py runserver
        ;;
    "frontend")
        echo "Iniciando servidor Vite..."
        cd frontend
        npm run dev
        ;;
    "install")
        echo "Instalando dependências do backend..."
        cd backend
        poetry install
        
        echo "Instalando dependências do frontend..."
        cd ../frontend
        npm install
        ;;
    "migrate")
        echo "Executando migrações do Django..."
        cd backend
        python manage.py migrate
        ;;
    "test")
        echo "Executando testes do backend..."
        cd backend
        python manage.py test
        ;;
    "help")
        show_help
        ;;
    *)
        echo "Comando desconhecido: $1"
        show_help
        exit 1
        ;;
esac 