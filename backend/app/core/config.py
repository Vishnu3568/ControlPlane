import os
from pathlib import Path
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

# Base directory for the backend (E:\Project Folder\Nitish WEEK 20\backend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Workspace root (E:\Project Folder\Nitish WEEK 20)
WORKSPACE_ROOT = BASE_DIR.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "ControlPlane"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server Binding
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = f"sqlite:///{WORKSPACE_ROOT / 'data' / 'database' / 'founder.db'}"
    
    # AI Integration (Optional)
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, str):
            if v.lower() in ("release", "false", "0", "prod", "production"):
                return False
            if v.lower() in ("true", "1", "debug", "dev", "development"):
                return True
            return False
        return bool(v)
    
    model_config = SettingsConfigDict(
        env_file=(str(WORKSPACE_ROOT / ".env"), str(BASE_DIR / ".env")),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure critical data directories exist
(WORKSPACE_ROOT / "data" / "database").mkdir(parents=True, exist_ok=True)
(WORKSPACE_ROOT / "data" / "notes").mkdir(parents=True, exist_ok=True)
(WORKSPACE_ROOT / "data" / "backups").mkdir(parents=True, exist_ok=True)
