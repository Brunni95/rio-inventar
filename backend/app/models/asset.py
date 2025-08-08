from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.session import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    inventory_number = Column(String, unique=True, index=True, nullable=False)
    serial_number = Column(String, unique=True, index=True)
    model = Column(String)
    department = Column(String)
    os_version = Column(String)
    installation_date = Column(Date)
    warranty_expiry = Column(Date)
    purchase_date = Column(Date)
    purchase_price = Column(Numeric(10, 2))
    notes = Column(Text)
    ip_address = Column(String)
    hostname = Column(String)
    mac_address = Column(String)
    room = Column(String)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id")) # GE�NDERT: von assigned_to zu user_id
    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    # --- Navigation Properties f�r einfachen Zugriff ---
    user = relationship("User")
    asset_type = relationship("AssetType")
    manufacturer = relationship("Manufacturer")
    status = relationship("Status")
    location = relationship("Location")
    supplier = relationship("Supplier")

