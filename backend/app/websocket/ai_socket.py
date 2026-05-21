from fastapi import WebSocket, WebSocketDisconnect
from httpx import AsyncClient
from ..core.config import settings


async def stream_ai_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_json()
            prompt = message.get("prompt")
            if not prompt:
                await websocket.send_json({"error": "Missing prompt"})
                continue

            url = f"{settings.AI_SERVICE_URL.rstrip('/')}/chat"
            async with AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", url, json={"prompt": prompt}) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_text():
                        if chunk:
                            await websocket.send_json({"data": chunk})
            await websocket.send_json({"data": "__complete__"})
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await websocket.send_json({"error": str(exc)})
        await websocket.close()
