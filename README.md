# 🚀 RIO-Inventar

Modernes Inventar-Management mit FastAPI (Backend) und Vue 3 (Frontend). Azure AD Login via MSAL, serverseitige Pagination/Sorting, Dashboard-Widgets und QR-Code-Export.

---

## ℹ️ Über das Projekt

**RIO-Inventar** ist eine moderne Webanwendung für den internen Gebrauch.  
Sie dient zur Verwaltung von Lagerbeständen, Artikelstammdaten und Inventarbewegungen.

🎯 **Ziele:**
- Produktives Werkzeug im Alltag
- Praxisnahes Ausbildungsprojekt für Lernende
- Demonstration moderner Technologien und Architekturprinzipien

---

## 🏗️ Architektur

Entkoppelt und skalierbar: FastAPI + SQLAlchemy + Alembic, Vue 3 + Router + Axios.

## Übersicht (Mermaid-Diagramm)

```mermaid
graph TD
    subgraph Frontend [Vue.js Frontend]
        A1[Suchleiste (Input)]
        A2[Filteroptionen (Dropdowns, Checkboxen)]
        A3[Suchresultate (Listendarstellung)]
        A4[Pagination-Komponente]
    end

    subgraph API [FastAPI Backend]
        B1[/api/v1/assets]
        B2[Auth: Azure AD JWT (JWKS)]
        B3[CRUD + Pagination + Sorting]
    end

    subgraph Backend [PostgreSQL + SQLAlchemy]
        C1[SQLAlchemy ORM]
        C2[Alembic Migrations]
        C3[Seed Script]
    end

    A1 --> B1
    A2 --> B1
    B1 --> B2 --> C2 --> C1
    C1 --> C3 --> B1
    B1 --> A3
    A3 --> A4
```

---

## Frontend (Vue.js)

- **Komponentenstruktur (Auszug)**
    - `HeaderLayout.vue`: Navigation, Login/Logout, Dark Mode Toggle
    - `DashboardView.vue`: KPI-Kacheln, Donut-Chart mit konfigurierbarer Gruppierung
    - `InventoryView.vue`: Serverseitige Pagination/Sorting, Formular, QR-Export, Historie
    - `components/Pagination.vue`: Wiederverwendbare Pagination
    - `components/charts/DonutChart.vue`: Farbstarke SVG-Donuts (HSL, Golden Angle)

- **Zustandsspeicherung**
    - Query-Parameter in der URL (z. B. `?q=test&page=2`)
    - Vue Router speichert Zustand für Zurücknavigation

---

## Backend (FastAPI)

- Endpoints `/api/v1/...` mit Schutz per Azure AD JWT
- Eager Loading gegen N+1, `skip`/`limit` + `order_by`/`order_dir`
- Alembic-Migrationen, `seed_db.py` für Demo-Daten

---

## Fehlerhandling
- Konsistente 400/401/409/500-Responses
- Logging und zentrale Error-Handler im Backend

---

## Qualität
- ESLint/Prettier im Frontend, Typhinweise + Pydantic im Backend

---

## Auth
- MSAL im Frontend (Popup/Silent), Token via Axios-Interceptor
- Backend: JWKS-Load, manuelle Audience/Issuer-Validierung

---

## Stack

| Bereich   | Technologie                 |
|-----------|-----------------------------|
| Frontend  | Vue 3, Vue Router, Axios    |
| Backend   | FastAPI, SQLAlchemy, Alembic|
| Datenbank | PostgreSQL                  |


