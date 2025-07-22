#!/bin/sh

# Dieses Skript aktiviert eine bestimmte Umgebungskonfiguration,
# indem es die entsprechende .env.<umgebung>-Datei nach .env kopiert.

# Bricht das Skript ab, wenn ein Befehl fehlschlägt
set -e

# Überprüft, ob ein Umgebungsname als Argument übergeben wurde
if [ -z "$1" ]; then
  echo "Fehler: Du musst eine Umgebung angeben (z.B. 'dev' oder 'prod')."
  echo "Beispiel: ./use-env.sh dev"
  exit 1
fi

ENVIRONMENT=$1
SOURCE_FILE=".env.${ENVIRONMENT}"

# Überprüft, ob die Quelldatei existiert
if [ -f "$SOURCE_FILE" ]; then
  # Kopiert die gewählte Konfigurationsdatei nach .env
  cp "$SOURCE_FILE" .env
  echo "✅ Umgebung '$ENVIRONMENT' wurde erfolgreich in .env aktiviert."
else
  echo "Fehler: Die Konfigurationsdatei '$SOURCE_FILE' wurde nicht gefunden."
  exit 1
fi