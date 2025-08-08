"""Generic CRUD base with typed helpers for SQLAlchemy models and Pydantic schemas."""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import Base  # for typing of bound models

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD-Objekt mit Standardmethoden zum Erstellen, Lesen, Aktualisieren, Löschen (CRUD).

        **Parameter**
        * `model`: Ein SQLAlchemy-Modellklasse
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        # SQLAlchemy 2.0: prefer Session.get for primary key lookups
        return db.get(self.model, id)

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # Convert Pydantic schema to dict
        obj_in_data = obj_in.model_dump()
        # Create SQLAlchemy model instance
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        # Update only explicitly set fields and ignore primary key
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Prevent accidental overwrite of primary key
        update_data.pop("id", None)

        for field_name, field_value in update_data.items():
            # Only set attributes that actually exist on the model
            if hasattr(db_obj, field_name):
                setattr(db_obj, field_name, field_value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        # SQLAlchemy 2.0: Session.get with None-handling
        obj = db.get(self.model, id)
        if obj is None:
            return None
        db.delete(obj)
        db.commit()
        return obj