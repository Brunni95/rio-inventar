from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    inventory_number = Column(String, unique=True, index=True, nullable=False)
    serial_number = Column(String, unique=True, index=True)
    model = Column(String)
    assigned_to = Column(String, index=True)
    department = Column(String)
    os_version = Column(String)
    installation_date = Column(Date)
    warranty_expiry = Column(Date)
    purchase_date = Column(Date)
    notes = Column(Text)
    ip_address = Column(String)
    hostname = Column(String)
    mac_address = Column(String)

    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    status_id = Column(Integer, ForeignKey("statuses.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    asset_type = relationship("AssetType")
    manufacturer = relationship("Manufacturer")
    status = relationship("Status")
    location = relationship("Location")
    supplier = relationship("Supplier")
