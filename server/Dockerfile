FROM python:3.12-slim

WORKDIR /server

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/venv

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run python -m scripts.create_session && uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]