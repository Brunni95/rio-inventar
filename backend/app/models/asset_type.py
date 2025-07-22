from sqlalchemy import Column, Integer, String
from app.db.session import Base

class AssetType(Base):
    __tablename__ = "asset_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

