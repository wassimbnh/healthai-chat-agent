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
uv sync --no-default-groups --group prod
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
