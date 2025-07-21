from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from crud import item as crud_item
from db.session import SessionLocal, engine
from auth import get_current_user, load_jwks # WICHTIG: Import von load_jwks

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RIO-Inventar API")

# WICHTIG: Dieser Block registriert die Funktion, die beim Start ausgeführt wird
@app.on_event("startup")
async def on_startup():
    await load_jwks()

# --- CORS Middleware ---
from fastapi.middleware.cors import CORSMiddleware
origins = ["http://localhost:5173", "http://localhost:8080"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Willkommen bei der RIO-Inventar API!"}

# --- API Endpunkte ---

@app.post("/api/v1/items", response_model=schemas.Item, status_code=201)
def create_item_endpoint(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_item = db.query(models.Item).filter(models.Item.sku == item.sku).first()
    if db_item:
        raise HTTPException(status_code=400, detail="SKU already registered")
    return crud_item.create_item(db=db, item=item)

@app.get("/api/v1/items", response_model=List[schemas.Item])
def get_items_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return items

@app.put("/api/v1/items/{item_id}", response_model=schemas.Item)
def update_item_endpoint(item_id: int, item_update: schemas.ItemCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud_item.update_item(db=db, db_item=db_item, item_update=item_update)

@app.delete("/api/v1/items/{item_id}", status_code=204)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_item = crud_item.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud_item.delete_item(db=db, db_item=db_item)
    return