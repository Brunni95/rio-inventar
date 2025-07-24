# Datei: backend/app/crud/supplier.py
from app.crud.base import CRUDBase
from app.models import Supplier
from app.schemas import SupplierCreate, SupplierUpdate

class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    # Hier können später modellspezifische CRUD-Methoden hinzugefügt werden.
    pass

# Wichtig: Erstelle eine Instanz, die in der API verwendet wird.
supplier = CRUDSupplier(Supplier)
