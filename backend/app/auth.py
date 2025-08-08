"""JWT-based auth with Azure AD (MSAL) validation and optional dev bypass."""
import os
import httpx
import asyncio
import logging
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.utils import base64url_decode
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import crud, schemas
from app.core.config import AZURE_TENANT_ID, AZURE_CLIENT_ID

logger = logging.getLogger(__name__)

DISABLE_AUTH = os.getenv("DISABLE_AUTH", "0") in ("1", "true", "True")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

ISSUER = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
OPENID_CONFIG_URL = f"{ISSUER}/.well-known/openid-configuration"

_JWKS: Optional[Dict[str, Any]] = None
_JWKS_URI: Optional[str] = None
_OPENID_ISSUER: Optional[str] = None
_JWKS_LOCK = asyncio.Lock()

async def load_jwks():
    """Load OpenID config and JWKS once and cache them."""
    global _JWKS, _JWKS_URI, _OPENID_ISSUER
    async with _JWKS_LOCK:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                if not _JWKS_URI or not _OPENID_ISSUER:
                    r = await client.get(OPENID_CONFIG_URL)
                    r.raise_for_status()
                    openid = r.json()
                    _JWKS_URI = openid["jwks_uri"]
                    _OPENID_ISSUER = openid.get("issuer")
                r2 = await client.get(_JWKS_URI)
                r2.raise_for_status()
                _JWKS = r2.json()
            logger.info("JWKS loaded successfully.")
        except Exception as e:
            logger.error("Failed to load JWKS: %s", e)
            _JWKS = None

def _get_key_for_kid(kid: str) -> Optional[Dict[str, str]]:
    if not _JWKS:
        return None
    for key in _JWKS.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None

def _rsa_public_key_from_jwk(jwk: Dict[str, str]):
    # jose can use JWK directly; pass it through
    return jwk

async def _ensure_jwks_loaded():
    if _JWKS is None:
        await load_jwks()
        if _JWKS is None:
            raise HTTPException(status_code=503, detail="JWKS keys are not loaded. Cannot validate token.")

async def get_current_active_user(
        db: Session = Depends(get_db),
        token: str = Depends(OAUTH2_SCHEME),
):
    # Dev bypass
    if DISABLE_AUTH:
        # Create/get a local dummy user for development
        dummy_oid = "00000000-0000-0000-0000-000000000000"
        user = crud.user.get_user_by_azure_oid(db, azure_oid=dummy_oid)
        if not user:
            user = crud.user.create_user(db, user=schemas.UserCreate(
                azure_oid=dummy_oid,
                email="dev@example.com",
                display_name="Dev User",
                department="DEV"
            ))
        return user

    if not AZURE_TENANT_ID or not AZURE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Azure config missing.")

    await _ensure_jwks_loaded()

    try:
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token header.")

        jwk = _get_key_for_kid(kid)
        if not jwk:
            # Key rollover? Reload JWKS and retry
            await load_jwks()
            jwk = _get_key_for_kid(kid)
            if not jwk:
                raise HTTPException(status_code=401, detail="Signing key not found.")

        public_key = _rsa_public_key_from_jwk(jwk)
        # Some python-jose versions expect a string for audience.
        # Disable built-in aud validation and validate manually.
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[jwk.get("alg", "RS256")],
            options={"verify_aud": False, "verify_iss": False},
        )

        # Manual audience validation against allowed values
        allowed_audiences = set()
        if AZURE_CLIENT_ID:
            allowed_audiences.add(AZURE_CLIENT_ID)
            allowed_audiences.add(f"api://{AZURE_CLIENT_ID}")

        aud_claim = payload.get("aud")
        if allowed_audiences:
            if isinstance(aud_claim, str):
                aud_ok = aud_claim in allowed_audiences
            elif isinstance(aud_claim, (list, tuple, set)):
                aud_ok = any(a in allowed_audiences for a in aud_claim)
            else:
                aud_ok = False
            if not aud_ok:
                logger.warning("Invalid audience. aud=%s allowed=%s", aud_claim, list(allowed_audiences))
                raise HTTPException(status_code=401, detail="Invalid audience.")

        # Manual issuer validation: prefer issuer from OpenID configuration
        iss_claim = payload.get("iss")
        expected_issuer = _OPENID_ISSUER or ISSUER
        if expected_issuer and iss_claim != expected_issuer:
            # Fallback: accept known tenant variants/domains
            tid = payload.get("tid")
            issuer_ok = False
            if isinstance(tid, str) and tid:
                domains = [
                    "https://login.microsoftonline.com",
                    "https://login.microsoftonline.de",
                    "https://login.windows.net",
                    "https://sts.windows.net",
                ]
                suffixes = [f"/{tid}/v2.0", f"/{tid}/", f"/{tid}"]
                candidates = {d + s for d in domains for s in suffixes}
                issuer_ok = iss_claim in candidates
                # Additionally: tolerate issuer mismatch when tenant-id matches
                if not issuer_ok and AZURE_TENANT_ID and tid == AZURE_TENANT_ID:
                    issuer_ok = True
            if not issuer_ok:
                logger.warning(
                    "Invalid issuer. iss=%s expected=%s candidates_example=%s",
                    iss_claim,
                    expected_issuer,
                    next(iter(candidates)) if 'candidates' in locals() and candidates else None,
                )
                raise HTTPException(status_code=401, detail="Invalid issuer.")

        azure_oid = payload.get("oid")
        if not azure_oid:
            raise HTTPException(status_code=401, detail="OID claim missing.")

        # User sync (create on first login)
        user = crud.user.get_user_by_azure_oid(db, azure_oid=azure_oid)
        if not user:
            email_claim = (
                payload.get("preferred_username")
                or payload.get("email")
                or payload.get("upn")
            )
            user = crud.user.create_user(db, user=schemas.UserCreate(
                azure_oid=azure_oid,
                email=email_claim,
                display_name=payload.get("name"),
                department=payload.get("department"),
            ))
        return user

    except JWTError as e:
        logger.warning("JWT decode failed: %s", e)
        raise HTTPException(status_code=401, detail="Invalid token.")
