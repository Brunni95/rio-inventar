# PowerShell-Skript zum kompletten Zurücksetzen und Füllen der Entwicklungs-Datenbank

Write-Host "--- Schritt 1: Stoppe alle Container und lösche das Datenbank-Volume ---" -ForegroundColor Yellow
docker-compose down -v

Write-Host "`n--- Schritt 2: Baue die Images neu und starte die Container im Hintergrund ---" -ForegroundColor Yellow
docker-compose up --build -d

Write-Host "`n--- Schritt 3: Warte 10 Sekunden, damit die Datenbank sicher gestartet ist ---" -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`n--- Schritt 5: Fülle die Datenbank mit Testdaten ---" -ForegroundColor Yellow
docker-compose exec backend python app/seed_db.py

Write-Host "`n✅ Prozess abgeschlossen! Deine Dev-Umgebung ist jetzt frisch und mit Testdaten gefüllt." -ForegroundColor Green
Write-Host "Du kannst jetzt auf http://localhost:5173 zugreifen."