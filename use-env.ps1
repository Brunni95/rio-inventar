# use-env.ps1

param (
    [string]$Environment
)

if (-not $Environment) {
    Write-Host "Fehler: Du musst eine Umgebung angeben (z.B. 'dev' oder 'prod')." -ForegroundColor Red
    Write-Host "Beispiel: .\use-env.ps1 dev"
    exit 1
}

$sourceFile = ".env.$Environment"

if (Test-Path $sourceFile) {
    Copy-Item -Path $sourceFile -Destination ".env" -Force
    Write-Host "Umgebung '$Environment' wurde erfolgreich in .env aktiviert." -ForegroundColor Green
} else {
    Write-Host "Fehler: Die Konfigurationsdatei '$sourceFile' wurde nicht gefunden." -ForegroundColor Red
    exit 1
}