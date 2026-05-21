import os
from pathlib import Path
from typing import Any
from httpx import AsyncClient, Response
from ..core.config import settings


async def proxy_ai_request(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{settings.AI_SERVICE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    async with AsyncClient(timeout=60.0) as client:
        response: Response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()


async def upload_pdf_to_ai(file_path: str, filename: str) -> dict[str, Any]:
    url = f"{settings.AI_SERVICE_URL.rstrip('/')}/upload-pdf"
    async with AsyncClient(timeout=120.0) as client:
        with open(file_path, "rb") as data:
            response = await client.post(url, files={"file": (filename, data, "application/pdf")})
        response.raise_for_status()
        return response.json()


async def ask_pdf_to_ai(document_id: int, question: str) -> dict[str, Any]:
    payload = {"document_id": document_id, "question": question}
    return await proxy_ai_request("ask-pdf", payload)


async def chat_with_ai(prompt: str) -> dict[str, Any]:
    return await proxy_ai_request("chat", {"prompt": prompt})


async def clear_ai_chat() -> dict[str, Any]:
    return await proxy_ai_request("clear-chat", {})
