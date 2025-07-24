# Datei: backend/app/crud/user.py
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_azure_oid(self, db: Session, *, azure_oid: str) -> User | None:
        """
        Sucht einen Benutzer anhand seiner eindeutigen Azure Object ID.
        """
        return db.query(User).filter(User.azure_oid == azure_oid).first()

    def create_user(self, db: Session, *, user: UserCreate) -> User:
        """
        Diese Methode ist ein Alias für die Standard-Create-Methode,
        um die Kompatibilität mit dem bestehenden Auth-Code zu wahren.
        """
        return self.create(db, obj_in=user)

# WICHTIG: Erstelle die Instanz, die in __init__.py importiert wird
user = CRUDUser(User)