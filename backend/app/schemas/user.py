from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    display_name: str | None = None
    department: str | None = None

class UserCreate(UserBase):
    azure_oid: str

class User(UserBase):
    id: int
    azure_oid: str

    class Config:
        from_attributes = True
