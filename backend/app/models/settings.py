from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime, timezone
from backend.app.core.database import Base

class AppSetting(Base):
    __tablename__ = "app_settings"
    
    key = Column(String(64), primary_key=True, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

