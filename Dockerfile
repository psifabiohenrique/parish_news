ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN uv sync
COPY . /code

ENV SECRET_KEY "gRhoM1F0xnxe02g4npp3AEvsYmytq2ELNGvMpA5XSsD6cU7GUK"
RUN uv run python manage.py migrate
RUN uv run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uv", "run", "gunicorn","--bind",":8000","--workers","2","paroquianews.wsgi"]
