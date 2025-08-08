"""Development seeding script: creates reference data and sample assets.

Note: This script truncates tables and inserts demo data for local development.
"""

from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.db.session import SessionLocal
from datetime import date
import random

def seed_db():
    db: Session = SessionLocal()

    print("--- STARTING DATABASE SEEDING ---")

    # Clear tables in the correct order to satisfy FK constraints
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

    # --- Create reference/master data ---
    print("2. Seeding master data...")

    # Locations
    location_zh = crud.location.create(db=db, obj_in=schemas.LocationCreate(name="Büro Zürich", description="Hauptsitz"))
    location_be = crud.location.create(db=db, obj_in=schemas.LocationCreate(name="Büro Bern", description="Zweigniederlassung"))
    location_lager = crud.location.create(db=db, obj_in=schemas.LocationCreate(name="Hauptlager", description="Keller UG"))

    # Manufacturers
    dell = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="Dell"))
    apple = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="Apple"))
    logitech = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="Logitech"))
    hp = crud.manufacturer.create(db=db, obj_in=schemas.ManufacturerCreate(name="HP"))

    # Statuses
    status_lager = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="An Lager"))
    status_betrieb = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="Im Betrieb"))
    status_reparatur = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="In Reparatur"))
    status_ausgemustert = crud.status.create(db=db, obj_in=schemas.StatusCreate(name="Ausgemustert"))

    # Suppliers
    lieferant_td = crud.supplier.create(db=db, obj_in=schemas.SupplierCreate(name="TechData AG"))
    lieferant_apple = crud.supplier.create(db=db, obj_in=schemas.SupplierCreate(name="Apple Business"))

    # Asset types
    typ_notebook = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Notebook"))
    typ_monitor = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Monitor"))
    typ_maus = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Maus"))
    typ_dock = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Dockingstation"))
    typ_keyboard = crud.asset_type.create(db=db, obj_in=schemas.AssetTypeCreate(name="Tastatur"))

    # --- Create users ---
    print("3. Seeding users...")
    # Replace OIDs with real values from your Azure AD tenant as needed.
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

    # --- Create a few sample assets ---
    print("4. Seeding 10+ assets...")

    # Assets for sample user 1
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-001", model="Latitude 7440", purchase_price=2200.50, serial_number="SN-DELL-001", purchase_date=date(2023, 10, 5), asset_type_id=typ_notebook.id, manufacturer_id=dell.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_td.id, user_id=user_lars.id), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-MON-005", model="UltraSharp U2723QE", purchase_price=850.00, serial_number="SN-DELL-002", purchase_date=date(2023, 10, 5), asset_type_id=typ_monitor.id, manufacturer_id=dell.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_td.id, user_id=user_lars.id), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-DOC-003", model="WD22TB4 Thunderbolt Dock", purchase_price=350.00, serial_number="SN-DELL-003", purchase_date=date(2023, 10, 5), asset_type_id=typ_dock.id, manufacturer_id=dell.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_td.id, user_id=user_lars.id), user_id=user_lars.id)

    # Assets for sample user 2
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-NB-002", model="MacBook Pro 16 M3", purchase_price=3500.00, serial_number="SN-APPLE-001", purchase_date=date(2023, 11, 15), asset_type_id=typ_notebook.id, manufacturer_id=apple.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_apple.id, user_id=user_martina.id), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-MON-008", model="Studio Display", purchase_price=1800.00, serial_number="SN-APPLE-002", purchase_date=date(2023, 11, 15), asset_type_id=typ_monitor.id, manufacturer_id=apple.id, status_id=status_betrieb.id, location_id=location_zh.id, supplier_id=lieferant_apple.id, user_id=user_martina.id), user_id=user_lars.id)

    # Assets for sample user 3
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-004", model="EliteBook 840 G10", purchase_price=1950.00, serial_number="SN-HP-001", purchase_date=date(2024, 1, 20), asset_type_id=typ_notebook.id, manufacturer_id=hp.id, status_id=status_betrieb.id, location_id=location_be.id, supplier_id=lieferant_td.id, user_id=user_peter.id), user_id=user_lars.id)

    # Assets in stock (no user)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-005", model="Latitude 7440", purchase_price=2200.50, serial_number="SN-DELL-004", purchase_date=date(2024, 3, 1), asset_type_id=typ_notebook.id, manufacturer_id=dell.id, status_id=status_lager.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-006", model="Latitude 7440", purchase_price=2200.50, serial_number="SN-DELL-005", purchase_date=date(2024, 3, 1), asset_type_id=typ_notebook.id, manufacturer_id=dell.id, status_id=status_lager.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-MOU-010", model="MX Master 3S", purchase_price=120.00, serial_number="SN-LOGI-001", purchase_date=date(2024, 2, 10), asset_type_id=typ_maus.id, manufacturer_id=logitech.id, status_id=status_lager.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)

    # Defective asset
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-KEY-007", model="MX Keys", purchase_price=130.00, serial_number="SN-LOGI-002", purchase_date=date(2022, 5, 5), asset_type_id=typ_keyboard.id, manufacturer_id=logitech.id, status_id=status_reparatur.id, location_id=location_lager.id, supplier_id=lieferant_td.id, user_id=None), user_id=user_lars.id)

    # Retired asset
    crud.asset.create_with_log(db=db, obj_in=schemas.AssetCreate(inventory_number="IT-LAP-OLD-099", model="MacBook Pro 2018", purchase_price=2800.00, serial_number="SN-APPLE-OLD", purchase_date=date(2018, 7, 15), asset_type_id=typ_notebook.id, manufacturer_id=apple.id, status_id=status_ausgemustert.id, location_id=location_lager.id, supplier_id=lieferant_apple.id, user_id=None), user_id=user_lars.id)

    # --- Additional bulk assets for pagination tests ---
    print("5. Seeding bulk assets for pagination...")
    bulk_count = 150
    asset_types = [typ_notebook, typ_monitor, typ_maus, typ_dock, typ_keyboard]
    manufacturers = [dell, apple, logitech, hp]
    statuses = [status_lager, status_betrieb, status_reparatur]
    locations = [location_zh, location_be, location_lager]
    users_list = [user_lars, user_martina, user_peter, None]

    # Find the next running index for inventory numbers
    start_index = 1000
    for i in range(bulk_count):
        idx = start_index + i
        at = random.choice(asset_types)
        man = random.choice(manufacturers)
        st = random.choice(statuses)
        loc = random.choice(locations)
        usr = random.choice(users_list)
        inv = f"IT-BULK-{idx:04d}"
        serial = f"SN-BULK-{idx:06d}"
        price = round(random.uniform(80, 3200), 2)
        model = (
            "Latitude" if man is dell else
            "MacBook" if man is apple else
            "MX" if man is logitech else
            "EliteBook"
        ) + f" {random.randint(1, 999)}"

        asset_in = schemas.AssetCreate(
            inventory_number=inv,
            serial_number=serial,
            model=model,
            purchase_price=price,
            purchase_date=date(2023, random.randint(1, 12), random.randint(1, 28)),
            asset_type_id=at.id,
            manufacturer_id=man.id,
            status_id=st.id,
            location_id=loc.id,
            supplier_id=lieferant_td.id,
            user_id=(usr.id if usr else None),
        )
        crud.asset.create_with_log(db=db, obj_in=asset_in, user_id=user_lars.id)

    db.close()
    print("--- DATABASE SEEDING COMPLETE ---")

if __name__ == "__main__":
    seed_db()