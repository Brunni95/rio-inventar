# in backend/app/seed_db.py

from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.db.session import SessionLocal
from datetime import date

def seed_db():
    db: Session = SessionLocal()

    print("--- STARTING DATABASE SEEDING ---")

    # Leere die Tabellen in der richtigen Reihenfolge
    print("1. Clearing existing data...")
    db.query(models.AssetLog).delete()
    db.query(models.Asset).delete()
    db.query(models.User).delete()
    db.query(models.Location).delete()
    db.query(models.Manufacturer).delete()
    db.query(models.Status).delete()
    db.query(models.Supplier).delete()
    db.query(models.AssetType).delete()
    db.commit()

    # --- Stammdaten erstellen ---
    print("2. Seeding master data...")

    # Standorte
    location_zh = crud.location.create(db=db, obj_in=schemas.LocationCreate(name="Büro Zürich", description="Hauptsitz"))
    location_be = crud.location.create(db=db, obj_in=schemas.LocationCreate(name="Büro Bern", description="Zweigniederlassung"))
    location_lager = crud.location.create(db=db, obj_in=schemas.LocationCreate(name="Hauptlager", description="Keller UG"))

    # Hersteller
    dell = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="Dell"))
    apple = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="Apple"))
    logitech = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="Logitech"))
    hp = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="HP"))

    # Status
    status_lager = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="An Lager"))
    status_betrieb = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="Im Betrieb"))
    status_reparatur = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="In Reparatur"))
    status_ausgemustert = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="Ausgemustert"))

    # Lieferanten
    lieferant_td = crud.supplier.create(db=db, obj_in=schemas.SupplierCreate(name="TechData AG"))
    lieferant_apple = crud.supplier.create(db=db, obj_in=schemas.SupplierCreate(name="Apple Business"))

    # Geräte-Typen
    typ_notebook = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Notebook"))
    typ_monitor = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Monitor"))
    typ_maus = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Maus"))
    typ_dock = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Dockingstation"))
    typ_keyboard = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Tastatur"))

    # --- Benutzer erstellen ---
    print("3. Seeding users...")
    # Wichtig: Ersetze die OIDs mit echten Werten aus deinem Azure AD Tenant.
    user_lars = crud.user.create_user(db, user=schemas.UserCreate(
        azure_oid="ea60d443-71b8-4121-8647-4ea830365524",
        email="l.brunner@deinedomain.com",
        display_name="Lars Brunner",
        department="IT"
    ))
    user_martina = crud.user.create_user(db, user=schemas.UserCreate(
        azure_oid="5327c84c-6121-47c7-b335-1b4b317558a6",
        email="m.muster@deinedomain.com",
        display_name="Martina Muster",
        department="Marketing"
    ))
    user_peter = crud.user.create_user(db, user=schemas.UserCreate(
        azure_oid="3ab87443-02e8-4432-8675-cdb73efe1cb7",
        email="p.pan@deinedomain.com",
        display_name="Peter Pan",
        department="Sales"
    ))

    # --- Assets erstellen ---
    print("4. Seeding 10+ assets...")

    # Assets für Lars Brunner
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-001", model="Latitude 7440", purchase_price=2200.50, serial_number="SN-DELL-001", purchase_date=date(2023, 10, 5), asset_type_id=typ_notebook.id, manufacturer_id=dell.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_td.id, user_id=user_lars.id), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-MON-005", model="UltraSharp U2723QE", purchase_price=850.00, serial_number="SN-DELL-002", purchase_date=date(2023, 10, 5), asset_type_id=typ_monitor.id, manufacturer_id=dell.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_td.id, user_id=user_lars.id), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-DOC-003", model="WD22TB4 Thunderbolt Dock", purchase_price=350.00, serial_number="SN-DELL-003", purchase_date=date(2023, 10, 5), asset_type_id=typ_dock.id, manufacturer_id=dell.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_td.id, user_id=user_lars.id), user_id=user_lars.id)

    # Assets für Martina Muster
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-NB-002", model="MacBook Pro 16 M3", purchase_price=3500.00, serial_number="SN-APPLE-001", purchase_date=date(2023, 11, 15), asset_type_id=typ_notebook.id, manufacturer_id=apple.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_apple.id, user_id=user_martina.id), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-MON-008", model="Studio Display", purchase_price=1800.00, serial_number="SN-APPLE-002", purchase_date=date(2023, 11, 15), asset_type_id=typ_monitor.id, manufacturer_id=apple.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_apple.id, user_id=user_martina.id), user_id=user_lars.id)

    # Assets für Peter Pan
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-004", model="EliteBook 840 G10", purchase_price=1950.00, serial_number="SN-HP-001", purchase_date=date(2024, 1, 20), asset_type_id=typ_notebook.id, manufacturer_id=hp.id, status_id=status_betrieb.id, location_id=location_be.id, supplier_id=lieferant_td.id, user_id=user_peter.id), user_id=user_lars.id)

    # Assets im Lager
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-005", model="Latitude 7440", purchase_price=2200.50, serial_number="SN-DELL-004", purchase_date=date(2024, 3, 1), asset_type_id=typ_notebook.id, manufacturer_id=dell.id, status_id=status_lager.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-006", model="Latitude 7440", purchase_price=2200.50, serial_number="SN-DELL-005", purchase_date=date(2024, 3, 1), asset_type_id=typ_notebook.id, manufacturer_id=dell.id, status_id=status_lager.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-MOU-010", model="MX Master 3S", purchase_price=120.00, serial_number="SN-LOGI-001", purchase_date=date(2024, 2, 10), asset_type_id=typ_maus.id, manufacturer_id=logitech.id, status_id=status_lager.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)

    # Defektes Asset
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-KEY-007", model="MX Keys", purchase_price=130.00, serial_number="SN-LOGI-002", purchase_date=date(2022, 5, 5), asset_type_id=typ_keyboard.id, manufacturer_id=logitech.id, status_id=status_reparatur.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)

    # Ausgemustertes Asset
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-OLD-099", model="MacBook Pro 2018", purchase_price=2800.00, serial_number="SN-APPLE-OLD", purchase_date=date(2018, 7, 15), asset_type_id=typ_notebook.id, manufacturer_id=apple.id, status_id=status_ausgemustert.id, location_id=location_lager.id, supplier_id=lieferant_apple.id, user_id=None), user_id=user_lars.id)

    db.close()
    print("--- DATABASE SEEDING COMPLETE ---")

if __name__ == "__main__":
    seed_db()