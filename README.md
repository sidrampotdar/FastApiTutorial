# AI Assistant Backend

Production-style FastAPI backend for an AI Assistant application.

## Features

- FastAPI with async PostgreSQL + SQLAlchemy
- JWT authentication with OAuth2
- Redis + Celery integration
- WebSocket streaming support
- PDF upload support
- Clean modular architecture
- Environment-based configuration via `.env`
- Docker + docker-compose ready
- Standardized API responses

## Quick Start

1. Copy `.env.example` to `.env` and update values.
2. Start services:
   ```bash
   docker compose up --build
   ```
3. Open API docs:
   - http://localhost:8000/docs
   - http://localhost:8000/redoc

## Environment Variables

Required values:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `AI_SERVICE_URL`
- `REDIS_URL`
- `FRONTEND_URL`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `ALGORITHM`

## API Endpoints

Auth:

- `POST /auth/register`
- `POST /auth/login`

Users:

- `GET /users/me`

Notes:

- `GET /notes`
- `POST /notes`
- `PUT /notes/{id}`
- `DELETE /notes/{id}`

Expenses:

- `GET /expenses`
- `POST /expenses`

AI:

- `POST /ai/chat`
- `POST /ai/upload-pdf`
- `POST /ai/ask-pdf`
- `POST /ai/clear-chat`

History:

- `GET /chat/history`

Health:

- `GET /health`

WebSocket:

- `GET /ws/ai`

## Notes

- The project is designed so that production deployment only requires changing environment values.
- Local development uses `docker compose` and local Postgres/Redis containers.
