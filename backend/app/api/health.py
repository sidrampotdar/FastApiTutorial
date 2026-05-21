from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return {"success": True, "data": {"status": "ok"}, "error": None}
