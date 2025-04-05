# ParoquiaNews

Sistema de gerenciamento de notícias e fotos para paróquias.

## Estrutura do Projeto

- `backend/`: API REST desenvolvida em Django
- `frontend/`: Aplicação web desenvolvida em React
- `mobile/`: Aplicativo mobile desenvolvido em React Native

## Requisitos

### Backend
- Python 3.8+
- Poetry (gerenciador de dependências)

### Frontend Web
- Node.js 14+
- npm ou yarn

### Mobile
- Node.js 14+
- npm ou yarn
- React Native CLI
- Android Studio (para Android)
- Xcode (para iOS)

## Instalação

### Backend
1. Instale o Poetry se ainda não tiver:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone o repositório e instale as dependências:
```bash
git clone [url-do-repositorio]
cd paroquianews
poetry install
```

3. Ative o ambiente virtual:
```bash
poetry shell
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Execute o servidor:
```bash
python manage.py runserver
```

### Frontend Web
1. Instale as dependências:
```bash
cd frontend
npm install
```

2. Execute o servidor de desenvolvimento:
```bash
npm start
```

### Mobile
1. Instale as dependências:
```bash
cd mobile
npm install
```

2. Execute o aplicativo:
```bash
npx react-native run-android  # Para Android
npx react-native run-ios      # Para iOS
```

## Funcionalidades

- Sistema de autenticação para membros da pastoral
- Gerenciamento de notícias
- Upload e gerenciamento de fotos
- Visualização pública de notícias e fotos
- Aplicativo mobile para acompanhamento das notícias

## Estrutura do Backend

O backend é desenvolvido em Django e inclui:

- API REST usando Django REST Framework
- Sistema de autenticação JWT
- Upload de arquivos com suporte a imagens
- Banco de dados PostgreSQL (configurável)
- Sistema de cache
- Documentação automática da API

## Contribuição

Para contribuir com o projeto, siga os passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request 