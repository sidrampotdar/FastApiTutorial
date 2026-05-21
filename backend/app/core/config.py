import os
from pathlib import Path
from pydantic import AnyUrl, BaseModel, Field
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BASE_DIR.parent
ENV_FILE = ROOT_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(dotenv_path=ENV_FILE)


class Settings(BaseModel):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AI_SERVICE_URL: AnyUrl
    REDIS_URL: str
    FRONTEND_URL: str
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "ai_assistant"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    class Config:
        env_prefix = ""
        case_sensitive = True


settings = Settings(**os.environ)
