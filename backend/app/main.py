from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from db.session import engine
from auth import load_jwks
from api.v1.endpoints import assets, locations, manufacturers, statuses, suppliers, asset_types

# Erstellt alle Datenbanktabellen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RIO-Inventar API")

# Lädt die Azure AD-Sicherheitsschlüssel beim Start
@app.on_event("startup")
async def on_startup():
    await load_jwks()

# CORS-Einstellungen
origins = ["http://localhost:5173", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Binde die Router für die einzelnen Modelle in die Haupt-App ein
api_prefix = "/api/v1"
app.include_router(assets.router, prefix=f"{api_prefix}/assets", tags=["Assets"])
app.include_router(locations.router, prefix=f"{api_prefix}/locations", tags=["Locations"])
app.include_router(manufacturers.router, prefix=f"{api_prefix}/manufacturers", tags=["Manufacturers"])
app.include_router(statuses.router, prefix=f"{api_prefix}/statuses", tags=["Statuses"])
app.include_router(suppliers.router, prefix=f"{api_prefix}/suppliers", tags=["Suppliers"])
app.include_router(asset_types.router, prefix=f"{api_prefix}/asset-types", tags=["Asset Types"])

@app.get("/")
def read_root():
    return {"message": "Willkommen bei der RIO-Inventar API!"}
