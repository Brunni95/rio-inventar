# in backend/app/auth.py

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import asyncio
from sqlalchemy.orm import Session

# Importiere unsere neuen CRUD-Funktionen, Schemas, Modelle und die DB-Session
from app import crud, schemas, models
from app.db.session import get_db
from app.core.config import AZURE_TENANT_ID, AZURE_CLIENT_ID

METADATA_URL = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0/.well-known/openid-configuration"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

jwks_cache = {}

async def load_jwks():
    global jwks_cache
    print("Loading JWKS keys from Azure (v2.0)...")
    async with httpx.AsyncClient() as client:
        try:
            metadata_response = await client.get(METADATA_URL)
            metadata_response.raise_for_status()
            jwks_uri = metadata_response.json()["jwks_uri"]

            jwks_response = await client.get(jwks_uri)
            jwks_response.raise_for_status()
            jwks_cache = {key["kid"]: key for key in jwks_response.json()["keys"]}
            print("JWKS keys loaded and cached successfully.")
        except (httpx.HTTPStatusError, KeyError) as e:
            print(f"Failed to load JWKS keys: {e}")
            jwks_cache = {}

async def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not jwks_cache:
            print("Error: JWKS keys are not loaded. Cannot validate token.")
            raise credentials_exception

        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if kid not in jwks_cache:
            print(f"Error: Key ID '{kid}' not found in JWKS cache.")
            raise credentials_exception

        rsa_key = jwks_cache[kid]

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=f"api://{AZURE_CLIENT_ID}",
            issuer=f"https://sts.windows.net/{AZURE_TENANT_ID}/"
        )

        azure_oid: str = payload.get("oid")
        if azure_oid is None:
            raise credentials_exception

    except JWTError as e:
        print(f"Token validation error: {e}")
        raise credentials_exception

    # --- BENUTZER-SYNCHRONISATION ---
    user = crud.user.get_user_by_azure_oid(db, azure_oid=azure_oid)

    if not user:
        print(f"New user with OID {azure_oid} detected. Creating local user record.")
        user_in = schemas.UserCreate(
            azure_oid=azure_oid,
            email=payload.get("upn") or payload.get("email"),
            display_name=payload.get("name"),
            department=payload.get("department")
        )
        user = crud.user.create_user(db, user=user_in)

    return user