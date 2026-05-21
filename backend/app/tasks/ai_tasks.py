import httpx
from .celery_app import celery_app
from ..core.config import settings


@celery_app.task(name="ai.process_chat_prompt")
def process_chat_prompt(prompt: str) -> dict:
    url = f"{settings.AI_SERVICE_URL.rstrip('/')}/chat"
    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, json={"prompt": prompt})
        response.raise_for_status()
        return response.json()
