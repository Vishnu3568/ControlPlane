from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    database_connected: bool
    offline_mode: bool
    timestamp: str

class SettingItem(BaseModel):
    key: str
    value: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
