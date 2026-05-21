from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .notes import router as notes_router
from .expenses import router as expenses_router
from .ai import router as ai_router
from .chat import router as chat_router
from .health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(notes_router)
api_router.include_router(expenses_router)
api_router.include_router(ai_router)
api_router.include_router(chat_router)
api_router.include_router(health_router)
