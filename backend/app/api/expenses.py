from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.session import get_db
from ..models.expense import Expense
from ..schemas.expense import ExpenseCreate, ExpenseRead
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=list[ExpenseRead])
async def list_expenses(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await session.execute(select(Expense).where(Expense.owner_id == current_user.id))
    return result.scalars().all()


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def create_expense(
    payload: ExpenseCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    expense = Expense(
        description=payload.description,
        amount=payload.amount,
        category=payload.category or "",
        owner_id=current_user.id,
    )
    session.add(expense)
    await session.commit()
    await session.refresh(expense)
    return expense
