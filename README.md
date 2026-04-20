# MamaHealth

## Table of contents

1. [How to run](#how-to-run)
2. [Design diagram](#design-diagram)
3. [Project architecture](#project-architecture)
4. [Design decisions](#design-decisions)

---

## How to run

### Frontend

```bash
cp client/.env.example client/.env
cd client && npm install && npx expo start
```

### Backend

```bash
docker compose up --build
```

## Design diagram


## Project architecture

- `/client` - Expo frontend
- `/server` - FastAPI backend
  - `chat/` - Chat service with interface + implementation
  - `config/` - Dependencies and database configuration
  - `message/` - Message repository (interface + implementation)
  - `session/` - Session repository (interface + implementation)
  - `test/` - Unit tests

## Design decisions

![alt text](mm-sys-design.png)

### Separation of concerns

The backend follows a layered architecture with clear separation between:

- **Routes** - Handle HTTP requests and responses
- **Services** - Contain business logic
- **Models** - Define database schemas

### Abstract layer

The application uses an abstract service layer to decouple business logic from specific implementations. This allows:
- Easy swapping of implementations (e.g., different LLM providers)
- Unit testing without dependencies
- Clear contracts between layers