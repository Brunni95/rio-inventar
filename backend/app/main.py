# Datei: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importiere die einzelnen Router-Objekte aus den Endpunkt-Dateien
from app.api.v1.endpoints import assets, locations, manufacturers, statuses, suppliers, asset_types, users
from app.auth import load_jwks

# Erstelle die FastAPI-App-Instanz
app = FastAPI(title="RIO-Inventar API")

# Lade die Azure AD-Sicherheitsschlüssel beim Start der Anwendung
@app.on_event("startup")
async def on_startup():
    await load_jwks()

# Konfiguriere CORS (Cross-Origin Resource Sharing), damit das Frontend
# mit dem Backend kommunizieren kann.
# Diese Einstellungen sind für die lokale Entwicklung korrekt.
origins = ["http://localhost:5173", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definiere das Basis-Präfix für alle API v1 Routen
api_prefix = "/api/v1"

# Binde die einzelnen Router in die Haupt-App ein.
# Jede Gruppe von Endpunkten (z.B. für Assets) wird unter ihrem eigenen Pfad registriert.
# WICHTIG: Keine globalen 'dependencies' hier einfügen. Die Authentifizierung
# wird pro Endpunkt in den jeweiligen Dateien gehandhabt.
app.include_router(assets.router, prefix=f"{api_prefix}/assets", tags=["Assets"])
app.include_router(locations.router, prefix=f"{api_prefix}/locations", tags=["Locations"])
app.include_router(manufacturers.router, prefix=f"{api_prefix}/manufacturers", tags=["Manufacturers"])
app.include_router(statuses.router, prefix=f"{api_prefix}/statuses", tags=["Statuses"])
app.include_router(suppliers.router, prefix=f"{api_prefix}/suppliers", tags=["Suppliers"])
app.include_router(asset_types.router, prefix=f"{api_prefix}/asset-types", tags=["Asset Types"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["Users"])


# Eine einfache Root-Route zum Testen, ob der Server läuft.
@app.get("/")
def read_root():
    return {"message": "Willkommen bei der RIO-Inventar API!"}