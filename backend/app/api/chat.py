from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.session import get_db
from ..models.chat import ChatMessage
from ..schemas.chat import ChatMessageRead
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/history", response_model=list[ChatMessageRead])
async def get_chat_history(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await session.execute(select(ChatMessage).where(ChatMessage.user_id == current_user.id).order_by(ChatMessage.created_at.desc()))
    return result.scalars().all()
