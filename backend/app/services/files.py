from pathlib import Path
from fastapi import UploadFile
from uuid import uuid4

BASE_UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


def ensure_upload_folder() -> Path:
    BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return BASE_UPLOAD_DIR


async def save_pdf_upload(upload_file: UploadFile) -> tuple[str, str]:
    ensure_upload_folder()
    file_suffix = Path(upload_file.filename).suffix or ".pdf"
    stored_name = f"{uuid4().hex}{file_suffix}"
    target_path = BASE_UPLOAD_DIR / stored_name

    with target_path.open("wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)

    return stored_name, str(target_path)
