from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def ensure_not_in_use(db: Session, *, model, fk_column, fk_id: int, entity_label: str) -> None:
    """Raise 409 if any asset references the entity via given foreign key column.

    Parameters
    - db: SQLAlchemy session
    - model: SQLAlchemy mapped class to check (e.g., models.Asset)
    - fk_column: Column attribute to filter on (e.g., models.Asset.location_id)
    - fk_id: ID of the entity to check
    - entity_label: Human readable label used in the error message
    """
    dependency = db.query(model).filter(fk_column == fk_id).first()
    if dependency:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{entity_label} with ID {fk_id} is still referenced and cannot be deleted.",
        )


