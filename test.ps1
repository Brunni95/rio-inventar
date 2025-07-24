# ==============================================================================
# FINAL PowerShell Script to fix Python Syntax in API Endpoints
#
# FUNKTION:
# Dieses Skript korrigiert einen Syntaxfehler, der durch ein vorheriges Skript
# verursacht wurde. Es ersetzt die PowerShell-Syntax ('-ne', '{', '}') mit der
# korrekten Python-Syntax ('!=', ':').
#
# WARNUNG: Dieses Skript überschreibt Dateien in 'backend/app/api/v1/endpoints'.
# ERSTELLE EIN BACKUP VOR DER AUSFÜHRUNG.
#
# Anleitung:
# 1. Öffne PowerShell.
# 2. Navigiere zum Root-Verzeichnis deines Projekts.
# 3. Kopiere und füge dieses Skript ein und drücke Enter.
# ==============================================================================

Write-Host "Starte das finale Syntax-Korrektur-Skript für die API-Endpunkte..." -ForegroundColor Yellow

# --- Definition der Endpunkte, die wir anpassen müssen ---
$endpoints = @(
    @{ Singular = "location";     Plural = "locations";     ClassName = "Location" },
    @{ Singular = "manufacturer"; Plural = "manufacturers"; ClassName = "Manufacturer" },
    @{ Singular = "status";       Plural = "statuses";      ClassName = "Status" },
    @{ Singular = "supplier";     Plural = "suppliers";     ClassName = "Supplier" },
    @{ Singular = "asset_type";   Plural = "asset-types";   ClassName = "AssetType" },
    @{ Singular = "user";         Plural = "users";         ClassName = "User" }
)

# --- Pfad definieren ---
$endpointsPath = ".\backend\app\api\v1\endpoints"

foreach ($endpoint in $endpoints) {
    $singular = $endpoint.Singular
    $plural = $endpoint.Plural
    $className = $endpoint.ClassName

    $fileName = if ($plural -eq "asset-types") { "asset_types" } else { $plural }
    $endpointFilePath = Join-Path $endpointsPath "$($fileName).py"

    $id_variable = "${singular}_id"
    $item_variable = "item_in"

    Write-Host "Korrigiere Syntax in '$($endpointFilePath)'..." -ForegroundColor Cyan

    if (Test-Path $endpointFilePath) {
        # --- Definiere den kompletten Inhalt mit korrekter Python-Syntax ---
        $endpointContent = @"
# Datei: backend/app/api/v1/endpoints/$($fileName).py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.session import get_db
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.$($className)])
def read_$($plural.Replace("-","_"))(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Ruft eine Liste von $($plural) ab.
    """
    items = crud.$($singular).get_multi(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schemas.$($className), status_code=status.HTTP_201_CREATED)
def create_$($singular)(
    *,
    db: Session = Depends(get_db),
    $($item_variable): schemas.$($className)Create,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Erstellt einen neuen $($singular).
    """
    return crud.$($singular).create(db=db, obj_in=$($item_variable))

@router.delete("/{$($id_variable)}", status_code=status.HTTP_204_NO_CONTENT)
def delete_$($singular)($($id_variable): int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Löscht einen $($singular).
    """
    # KORREKTE PYTHON-SYNTAX: '!=' und ':'
    if "$($className)" != "User":
        asset_dependency = db.query(models.Asset).filter(getattr(models.Asset, '$($id_variable)') == $($id_variable)).first()
        if asset_dependency:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"$($className) mit ID {$($id_variable)} ist noch bei einem Asset in Verwendung und kann nicht gelöscht werden."
            )

    db_item = crud.$($singular).remove(db=db, id=$($id_variable))

    if not db_item:
        raise HTTPException(status_code=404, detail="$($className) not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
"@
        Set-Content -Path $endpointFilePath -Value $endpointContent -Encoding UTF8
        Write-Host "  [OK] Syntax in '$($endpointFilePath)' wurde erfolgreich korrigiert." -ForegroundColor Green
    } else {
        Write-Host "  [FEHLER] Endpunkt-Datei '$($endpointFilePath)' nicht gefunden. Übersprungen." -ForegroundColor Red
    }
}

Write-Host "Alle Endpunkte wurden syntaktisch korrigiert." -ForegroundColor Yellow
Write-Host "Bitte führe nun den folgenden Befehl aus, um alles ein letztes Mal neu zu bauen:" -ForegroundColor Cyan
Write-Host "docker-compose up --build --force-recreate"