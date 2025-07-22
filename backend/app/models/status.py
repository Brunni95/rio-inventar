from sqlalchemy import Column, Integer, String
from db.session import Base

class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
