from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .core.config import settings
from .core.logging import configure_logging
from .services.files import ensure_upload_folder
from .websocket.ai_socket import stream_ai_websocket


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="AI Assistant Backend",
        description="Modular FastAPI backend for AI assistant applications.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.on_event("startup")
    async def on_startup() -> None:
        ensure_upload_folder()

    @app.websocket("/ws/ai")
    async def websocket_endpoint(websocket: WebSocket):
        await stream_ai_websocket(websocket)

    return app


app = create_app()
