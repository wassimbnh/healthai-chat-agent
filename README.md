# Backend setup

This project uses [`uv`](https://docs.astral.sh/uv/) to manage Python dependencies.

## Requirements

- Python 3.12+
- `uv` installed locally

Please install `uv` if needed

## Create a virtual environment

Create a local virtual environment from the project root:

```bash
uv venv
```

Activate it in PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

## Install dependencies

Install development dependencies only. This also installs the default `dev` group:

```bash
uv sync
```

Install production dependencies only:

```bash
uv sync --group prod
```

## Groq Configuration

This project uses Groq's Llama model. You need a Groq API key.

1.  Get an API key from [Groq](https://console.groq.com/).
2.  Update the `.env` file in the `server/` directory:

```bash
GROQ_API_KEY=your_api_key_here
LLM_MODEL=llama-3.1-8b-instant
```

## Run the backend

Start the FastAPI server from the `server` directory:

```bash
cd server
uv run fastapi dev
```

Or, using uvicorn directly:

```bash
cd server
uv run uvicorn main:app --reload
```

Install both development and production dependencies:

```bash
uv sync --group prod
```

## Run the backend

Start the FastAPI server from the project root:

```bash
uv run --group prod fastapi dev
```

## Scripts

### Create Session Script

Creates a session with a hardcoded ID (useful for development/testing):

```bash
cd server
.venv\Scripts\python.exe scripts/create_session.py
```

The hardcoded session ID is: `00000000-0000-0000-0000-000000000001`
