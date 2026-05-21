from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..schemas.token import Token
from ..schemas.user import UserCreate, UserRead
from ..services.auth import authenticate_user, create_access_token, create_user, get_user_by_email
from ..utils.dependencies import get_current_user
from ..utils.exceptions import conflict_error
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate, session: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(session, user_create.email)
    if existing_user:
        raise conflict_error("A user with this email already exists")
    user = await create_user(session, user_create.email, user_create.password)
    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user
