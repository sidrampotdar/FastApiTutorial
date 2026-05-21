from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(..., max_length=200)
    content: str | None = None


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str | None = None
    owner_id: int

    model_config = {"from_attributes": True}
