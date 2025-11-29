# Frontend Technologie-Stack

Dieses Dokument beschreibt den gewählten Technologie-Stack für das **Service-Orientierte Firewall Management System**. Die Auswahl der Technologien basiert auf den Anforderungen an Performance, Skalierbarkeit, Wartbarkeit und Developer Experience (DX).

## 1. Core Framework & Sprache

### **React 18+**
- **Warum:** React ist der Industriestandard für moderne Webanwendungen. Version 18 bringt wichtige Features wie Automatic Batching und Concurrent Features, die für die Performance bei vielen Updates (z.B. in Dashboards) wichtig sind.
- **Einsatz:** Komponentenbasierte UI-Entwicklung, Virtual DOM für effiziente Updates.

### **TypeScript**
- **Warum:** Essenziell für ein Projekt dieser Größe und Komplexität. Die strikte Typisierung verhindert Laufzeitfehler, verbessert die Code-Qualität und bietet hervorragende IDE-Unterstützung (Autocompletion, Refactoring).
- **Einsatz:** Typisierung aller Komponenten, Props, State und API-Antworten (Interfaces für Services, Hosts, Policies etc.).

## 2. Build Tool & Entwicklungsumgebung

### **Vite**
- **Warum:** Vite ist extrem schnell im Vergleich zu älteren Tools wie Webpack (Create React App). Es bietet fast sofortigen Server-Start und Hot Module Replacement (HMR), was die Entwicklungsgeschwindigkeit massiv erhöht.
- **Einsatz:** Dev-Server, Building für Production, Optimierung der Assets.

## 3. Routing & Navigation

### **React Router v6**
- **Warum:** Der Standard für Routing in React. Version 6 bietet eine saubere API für verschachtelte Routen (Nested Routes), was perfekt für unsere Service-Hierarchie ist (`/services/:id/hosts`).
- **Einsatz:**
  - Globale Navigation (Dashboard, Services, Global Views)
  - Service-spezifische Navigation (Tabs innerhalb eines Services)
  - URL-Parameter Management (`:serviceId`)

## 4. State Management

Wir verwenden einen hybriden Ansatz, um UI-State und Server-State zu trennen:

### **Zustand (UI State)**
- **Warum:** Eine minimalistische, aber mächtige State-Management-Bibliothek. Viel einfacher und weniger Boilerplate als Redux. Perfekt für client-seitigen State.
- **Einsatz:**
  - Sidebar Status (collapsed/expanded)
  - Aktuelles Theme (Dark/Light Mode)
  - Aktuell ausgewählter Service (für Context)
  - Filter-Einstellungen in Tabellen

### **TanStack Query (ehemals React Query) (Server State)**
- **Warum:** Die beste Lösung für das Management von asynchronen Server-Daten. Es übernimmt Caching, Deduplizierung, Background-Updates und Fehlerbehandlung automatisch.
- **Einsatz:**
  - Laden von Service-Listen, Hosts, Policies
  - Caching von API-Antworten (verhindert unnötige Requests)
  - Optimistic Updates bei Änderungen (z.B. Policy löschen)
  - Loading- und Error-States

## 5. Styling & UI Components

### **Tailwind CSS**
- **Warum:** Ein Utility-First CSS Framework, das schnelle UI-Entwicklung ermöglicht. Es verhindert "CSS-Spaghetti", macht Styles direkt im HTML sichtbar und bietet ein konsistentes Design-System.
- **Einsatz:** Layouts, Spacing, Farben, Typografie, Responsive Design.

### **Headless UI**
- **Warum:** Eine Bibliothek von ungestylten, vollständig zugänglichen UI-Komponenten (von den Machern von Tailwind). Sie bietet die Logik für komplexe Komponenten, überlässt das Styling aber uns (via Tailwind).
- **Einsatz:** Modals, Dropdowns, Tabs, Toggles, Popover.

## 6. Visualisierung

### **React Flow**
- **Warum:** Eine spezialisierte Bibliothek für knotenbasierte Graphen. Perfekt geeignet, um Netzwerktopologien und Policy-Beziehungen zu visualisieren.
- **Einsatz:**
  - Visualisierung der Service-Architektur (Hosts, Networks)
  - Darstellung von Policy-Flüssen (Source -> Service -> Destination)
  - Interaktive Graphen (Zoom, Pan, Node-Click)

## 7. Data Fetching & Kommunikation

### **Axios**
- **Warum:** Ein bewährter HTTP-Client. Bietet Vorteile gegenüber `fetch` wie automatische JSON-Transformation, Interceptors (für Auth-Token oder globales Error-Handling) und Request-Cancellation.
- **Einsatz:** Kommunikation mit der REST API.

## 8. Testing & Qualitätssicherung

### **Vitest**
- **Warum:** Ein Unit-Test-Framework, das nativ mit Vite integriert ist. Es ist kompatibel mit Jest, aber viel schneller.
- **Einsatz:** Unit-Tests für Logik, Hooks und Utilities.

### **React Testing Library**
- **Warum:** Testet Komponenten aus der Sicht des Benutzers (z.B. "Klicke auf Button X"), statt Implementierungsdetails zu testen.
- **Einsatz:** Integrationstests für Komponenten und User-Flows.

---

## Zusammenfassung

Dieser Stack ist **modern, performant und zukunftssicher**. Er ist speziell darauf ausgelegt, die Herausforderungen einer komplexen, datenintensiven Anwendung wie dem Firewall Management System zu lösen:

- **Performance:** Vite + React 18 + Virtualisierung (für große Tabellen)
- **Komplexität:** TypeScript + Service-Orientierte Architektur
- **Daten-Management:** TanStack Query (Caching, Sync)
- **Visualisierung:** React Flow
