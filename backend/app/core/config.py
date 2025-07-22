# in backend/app/core/config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")