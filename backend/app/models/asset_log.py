from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base
from sqlalchemy.orm import relationship

class AssetLog(Base):
    __tablename__ = "asset_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String, nullable=False)
    field_changed = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    notes = Column(String)

    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    changed_by_user = relationship("User")
