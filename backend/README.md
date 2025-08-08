# Backend overview

FastAPI + SQLAlchemy backend with Azure AD JWT auth, Alembic migrations, and modular CRUD.

Highlights
- Auth: Azure AD JWT validation with JWKS, manual audience/issuer checks and optional dev-bypass
- API: Modular routers under `/api/v1`, unified dependency checks for DELETE
- Data: SQLAlchemy 2.x patterns, eager loading to avoid N+1
- Migrations: Alembic; run on container start via `entrypoint.sh`

Local development
- Environment via `.env` (AZURE_TENANT_ID, AZURE_CLIENT_ID, DATABASE_URL, DISABLE_AUTH)
- `seed_db.py` to populate demo data

Pagination & sorting
- Assets endpoint supports `skip`, `limit`, `search`, `order_by`, `order_dir`


