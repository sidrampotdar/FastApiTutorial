from fastapi import APIRouter, Depends
from ..schemas.user import UserRead
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user
