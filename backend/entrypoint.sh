#!/bin/sh

# Bricht das Skript ab, wenn ein Befehl fehlschlägt
set -e

# Warte kurz, um sicherzustellen, dass die Datenbank bereit ist
# (In echten Produktionsumgebungen würde man hier ein robustes "wait-for-it"-Skript verwenden)
sleep 5

# Führe die Datenbank-Migrationen aus
echo "Running database migrations..."
alembic upgrade head

# Führe den Befehl aus, der dem Skript übergeben wurde (das ist unser uvicorn-Befehl aus dem Dockerfile)
echo "Starting application..."
exec "$@"