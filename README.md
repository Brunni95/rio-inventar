# 🚀 RIO-Inventar

Ein internes Inventar-Management-Tool zur effizienten Verwaltung von Artikeln, Beständen und Standorten.

---

## ℹ️ Über das Projekt

**RIO-Inventar** ist eine moderne Webanwendung für den internen Gebrauch.  
Sie dient zur Verwaltung von Lagerbeständen, Artikelstammdaten und Inventarbewegungen.

🎯 **Ziele:**
- Produktives Werkzeug im Alltag
- Praxisnahes Ausbildungsprojekt für Lernende
- Demonstration moderner Technologien und Architekturprinzipien

---

## 🏗️ Softwarearchitektur

Die Anwendung basiert auf einer entkoppelten, skalierbaren Architektur.

## Übersicht (Mermaid-Diagramm)

```mermaid
graph TD
    subgraph Frontend [Vue.js Frontend]
        A1[Suchleiste (Input)]
        A2[Filteroptionen (Dropdowns, Checkboxen)]
        A3[Suchresultate (Listendarstellung)]
        A4[Pagination-Komponente]
    end

    subgraph API Gateway [Node.js Express API]
        B1[/search Endpoint]
        B2[Middleware: Logging & Fehlerbehandlung]
    end

    subgraph Backend [MongoDB + Services]
        C1[MongoDB: Artikelsammlung]
        C2[Suchservice (Query Builder)]
        C3[Response Mapper]
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

- **Komponentenstruktur**
    - `SearchInput.vue`: Textfeld mit v-model für Volltextsuche
    - `SearchFilters.vue`: Kombinierbare Filter wie Kategorie, Autor, Datum
    - `SearchResults.vue`: Listet Artikel mit Pagination
    - `Pagination.vue`: Steuerung der Seiten

- **Zustandsspeicherung**
    - Query-Parameter in der URL (z. B. `?q=test&page=2`)
    - Vue Router speichert Zustand für Zurücknavigation

---

## Backend (Node.js API + MongoDB)

- **Express Endpoint `/api/search`**
    - Nimmt Query-Parameter entgegen (`q`, `filters`, `page`, `limit`)
    - Validierung und Logging in Middleware
    - Ruft Suchlogik im Service auf

- **Suchlogik (Query Builder)**
    - Dynamisch generierte MongoDB-Abfrage mit:
        - `$text`-Suche für Volltext
        - Kombinierte Filter mit `$and`, `$or`
        - `skip` und `limit` für Pagination

- **Response Mapping**
    - Transformiert Daten in frontend-kompatibles Format
    - Enthält Trefferanzahl und Meta-Infos für Pagination

---

## Fehlerhandling

- Fehlercodes:
    - `400`: Ungültige Query-Parameter
    - `500`: Serverfehler (z. B. bei Mongo-Ausfall)

- Logging via Winston oder einheitliche Middleware

---

## Tests & Qualität

- **Unit Tests**
    - Für Query Builder und Response Mapper
- **Integrationstests**
    - End-to-End-Test über Cypress oder Postman
- **Performance**
    - Analyse über `explain()` in MongoDB
    - Optimierung bei häufigen redundanten Calls

---

## Zustände bei Navigation

- Vue Router speichert Suchstatus (Query-Parameter)
- "Zurück"-Button stellt Filter und Resultate korrekt wieder her

---

## Technologiestack

| Bereich      | Technologie        |
|-------------|--------------------|
| Frontend     | Vue.js 3, Vue Router |
| Backend      | Node.js, Express    |
| Datenbank    | MongoDB             |
| Tests        | Jest, Supertest     |
| Logging      | Winston             |


