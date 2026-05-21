from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..models.pdf_document import PDFDocument
from ..schemas.ai import AIRequest, AskPDFRequest
from ..utils.dependencies import get_current_user
from ..services.ai import chat_with_ai, upload_pdf_to_ai, ask_pdf_to_ai, clear_ai_chat
from ..services.files import save_pdf_upload
from ..utils.exceptions import resource_not_found

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat")
async def chat(payload: AIRequest, current_user=Depends(get_current_user)):
    response = await chat_with_ai(payload.prompt)
    return {"success": True, "data": response, "error": None}


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    filename, stored_path = await save_pdf_upload(file)
    document = PDFDocument(
        filename=filename,
        stored_path=stored_path,
        uploaded_by=current_user.id,
    )
    session.add(document)
    await session.commit()
    await session.refresh(document)
    ai_response = await upload_pdf_to_ai(stored_path, file.filename)
    return {"success": True, "data": {"document_id": document.id, "remote": ai_response}, "error": None}


@router.post("/ask-pdf")
async def ask_pdf(payload: AskPDFRequest, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    result = await session.get(PDFDocument, payload.document_id)
    if not result or result.uploaded_by != current_user.id:
        raise resource_not_found("PDF document not found")
    response = await ask_pdf_to_ai(payload.document_id, payload.question)
    return {"success": True, "data": response, "error": None}


@router.post("/clear-chat")
async def clear_chat(current_user=Depends(get_current_user)):
    response = await clear_ai_chat()
    return {"success": True, "data": response, "error": None}
