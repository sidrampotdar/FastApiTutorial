from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class UploadedPDFRequest(BaseModel):
    title: str | None = None


class AskPDFRequest(BaseModel):
    document_id: int
    question: str = Field(..., min_length=1)


class APIResponse(BaseModel):
    success: bool
    data: dict | list | None = None
    error: str | None = None
