# Asset endpoints: list, CRUD, logs, QR-code
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from app import crud, models, schemas
from app.auth import get_current_active_user
from app.db.session import get_db
import io
import segno

router = APIRouter()


@router.get("/", response_model=schemas.AssetList)
def read_assets(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = Query(None, description="Suche nach Inventarnr, Modell, Hostname oder Benutzername"),
        order_by: Optional[str] = Query("id", description="Sort key: e.g. inventory_number, manufacturer.name"),
        order_dir: Optional[str] = Query("desc", description="asc|desc"),
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Return assets with optional search, server-side sorting and pagination.

    Parameters:
    - db: SQLAlchemy session dependency
    - skip: Number of items to skip (offset)
    - limit: Maximum number of items to return
    - search: Optional free-text filter on several fields
    - order_by: Sort key (whitelisted)
    - order_dir: Sort direction ("asc" or "desc")
    - current_user: Authenticated user dependency

    Returns:
    - AssetList: Items and total count for pagination
    """
    allowed_order = {
        "id",
        "inventory_number",
        "model",
        "hostname",
        "serial_number",
        "asset_type.name",
        "manufacturer.name",
        "location.name",
        "status.name",
        "user.display_name",
    }
    if order_by not in allowed_order:
        raise HTTPException(status_code=400, detail=f"Invalid order_by '{order_by}'. Allowed: {sorted(list(allowed_order))}")
    items = crud.asset.get_multi_with_search(
        db,
        skip=skip,
        limit=limit,
        search=search,
        order_by=order_by or "id",
        order_dir=order_dir or "desc",
    )
    total = crud.asset.count_with_search(db, search=search)
    return {"items": items, "total": total}


@router.post("/", response_model=schemas.Asset, status_code=status.HTTP_201_CREATED)
def create_asset(
        *,
        db: Session = Depends(get_db),
        asset_in: schemas.AssetCreate,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new asset and record a CREATE log entry.

    Parameters:
    - db: SQLAlchemy session dependency
    - asset_in: Asset payload
    - current_user: Authenticated user dependency

    Returns:
    - Asset: Created asset
    """
    asset = crud.asset.create_with_log(db=db, obj_in=asset_in, user_id=current_user.id)
    return asset


@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Return an asset by its ID.

    Parameters:
    - db: SQLAlchemy session dependency
    - asset_id: Asset primary key
    - current_user: Authenticated user dependency

    Returns:
    - Asset: The requested asset

    Raises:
    - HTTPException 404: If asset does not exist
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.get("/{asset_id}/logs", response_model=List[schemas.AssetLog])
def read_asset_logs(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Return the change history (log entries) for a given asset.

    Parameters:
    - db: SQLAlchemy session dependency
    - asset_id: Asset primary key
    - current_user: Authenticated user dependency

    Returns:
    - list[AssetLog]: Log entries ordered by insertion

    Raises:
    - HTTPException 404: If asset does not exist
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return crud.asset_log.get_by_asset(db=db, asset_id=asset_id)


@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        asset_in: schemas.AssetUpdate,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an asset and write UPDATE log entries for changed fields.

    Parameters:
    - db: SQLAlchemy session dependency
    - asset_id: Asset primary key
    - asset_in: Partial update payload
    - current_user: Authenticated user dependency

    Returns:
    - Asset: Updated asset

    Raises:
    - HTTPException 404: If asset does not exist
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    asset = crud.asset.update_with_log(db=db, db_obj=asset, obj_in=asset_in, user_id=current_user.id)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete an asset along with its dependent logs.

    Parameters:
    - db: SQLAlchemy session dependency
    - asset_id: Asset primary key
    - current_user: Authenticated user dependency

    Returns:
    - 204 No Content on success

    Raises:
    - HTTPException 404: If asset does not exist
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    crud.asset.remove(db=db, id=asset_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{asset_id}/qrcode")
def get_asset_qr(
        *,
        db: Session = Depends(get_db),
        asset_id: int,
        current_user: models.User = Depends(get_current_active_user)
):
    """
    Return a PNG QR-code for the asset's inventory number.

    Parameters:
    - db: SQLAlchemy session dependency
    - asset_id: Asset primary key
    - current_user: Authenticated user dependency

    Returns:
    - StreamingResponse: PNG image with QR code

    Raises:
    - HTTPException 404: If asset does not exist
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    qr = segno.make(asset.inventory_number or str(asset_id))
    buf = io.BytesIO()
    qr.save(buf, kind='png', scale=6, border=2)
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')