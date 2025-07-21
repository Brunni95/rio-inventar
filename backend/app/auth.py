import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import asyncio

TENANT_ID = "3f27241d-d949-4cf1-a670-1c492efb689c"
CLIENT_ID = "168b7935-19c0-4a74-9df8-66f288175948"

# v1.0 Metadaten-URL (ohne /v2.0)
METADATA_URL = f"https://login.microsoftonline.com/{TENANT_ID}/.well-known/openid-configuration"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

jwks_cache = {}

async def load_jwks():
    global jwks_cache
    print("Loading JWKS keys from Azure (v1.0)...")
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

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not jwks_cache:
            raise credentials_exception

        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if kid not in jwks_cache:
            raise credentials_exception

        rsa_key = jwks_cache[kid]

        # v1.0 Issuer URL
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=f"api://{CLIENT_ID}", # <-- KORREKT
            issuer=f"https://sts.windows.net/{TENANT_ID}/"
        )
        return payload
    except JWTError as e:
        print(f"Token validation error: {e}")
        raise credentials_exception