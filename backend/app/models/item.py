from sqlalchemy import Column, Integer, String, Text
from db.session import Base # <-- HIER IST DIE KORREKTUR

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, default=0)