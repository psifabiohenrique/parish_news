FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app


# Copiar arquivos de dependências
COPY pyproject.toml .
COPY .python-version .

# Criar ambiente virtual e instalar dependências
RUN uv sync

# Copiar projeto
COPY . .

# Coletar arquivos estáticos
RUN uv run python manage.py collectstatic