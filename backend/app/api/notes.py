from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db.session import get_db
from ..models.note import Note
from ..schemas.note import NoteCreate, NoteRead, NoteUpdate
from ..utils.dependencies import get_current_user
from ..utils.exceptions import resource_not_found
from ..utils.response import success_response

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteRead])
async def read_notes(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await session.execute(select(Note).where(Note.owner_id == current_user.id))
    return result.scalars().all()


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = Note(title=payload.title, content=payload.content or "", owner_id=current_user.id)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


@router.put("/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = select(Note).where(Note.id == note_id, Note.owner_id == current_user.id)
    result = await session.execute(query)
    note = result.scalars().first()
    if not note:
        raise resource_not_found("Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    await session.commit()
    await session.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await session.execute(select(Note).where(Note.id == note_id, Note.owner_id == current_user.id))
    note = result.scalars().first()
    if not note:
        raise resource_not_found("Note not found")
    await session.delete(note)
    await session.commit()
    return None
