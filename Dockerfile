FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

VOLUME [ "/app/config" ]

CMD [ "uv", "run", "src/main.py"]
