# Service-Oriented Firewall Management UI

> **Modern React-basierte Benutzeroberfläche** für das Capirca Firewall Management System

![Version](https://img.shields.io/badge/version-0.2.0-blue)
![Status](https://img.shields.io/badge/status-in_development-yellow)
![React](https://img.shields.io/badge/React-19.2-61dafb)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)

## 🎯 Übersicht

Dieses Frontend implementiert ein **service-orientiertes** Design für die Verwaltung von Firewall-Regeln. Services (wie ATREMOTE, AD, MOODLE, SAP) sind die zentrale Organisationseinheit – jeder Service hat seine eigenen Hosts, Networks, Groups und Policies.

### Hauptfeatures

✅ **Service-First Architecture** - Services als Top-Level-Organisationseinheit  
✅ **Modern Dark Mode UI** - Glassmorphism Design mit Tailwind CSS  
✅ **Interactive Dashboard** - Live Stats, Health Monitoring, Activity Timeline  
✅ **Multi-View** - Grid/List Ansichten für Services  
✅ **Service Detail Views** - Dedizierte Tabs für Hosts, Networks, Groups, Policies  
✅ **Smart Search & Filters** - Schnelle Navigation durch Services  
✅ **Expiration Alerts** - Warnungen für ablaufende Policies  

## 🚀 Quick Start

```bash
# Dependencies installieren
npm install

# Development Server starten (http://localhost:5173)
npm run dev

# Production Build erstellen
npm run build
```

## 📸 Screenshots

### Dashboard
> Service Health Overview, Stats Cards, Top Services Chart, Recent Activity

*(Dashboard zeigt aggregierte Statistiken über alle Services: 10 Services, 127 Hosts, 48 Networks, 45 Groups, 297 Policies)*

### Services Overview
> Grid/List Views mit Search und Status-Indikatoren

*(Service Cards zeigen Kurzname, Status (healthy/warning/critical), Resource-Counts und Expiration Warnings)*

### Service Detail View
> Tabbed Interface mit Hosts, Networks, Groups, Policies

*(Jeder Service hat dedizierte Tabs mit vollständigen Tabellen für alle zugehörigen Entitäten)*

## 📂 Projekt-Struktur

```
frontend/
├── src/
│   ├── components/       # Wiederverwendbare UI-Komponenten
│   │   ├── common/       # ServiceBadge, StatusIndicator
│   │   ├── layout/       # AppLayout, Header, Sidebar
│   │   ├── dashboard/    # Dashboard-Widgets
│   │   └── services/     # Service-spezifische Komponenten
│   ├── pages/            # Routen-Seiten (Dashboard, Services, ServiceDetail)
│   ├── hooks/            # Custom React Hooks (useServices, useDashboard)
│   ├── data/             # Mock Data & API (10 Services, 16 Hosts, etc.)
│   ├── store/            # Zustand State Management (UI State)
│   ├── types/            # TypeScript Type Definitions
│   └── App.jsx           # Router + QueryClient Setup
└── package.json
```

## 🛠 Tech Stack

| Technologie | Version | Zweck |
|-------------|---------|-------|
| **React** | 19.2 | UI Framework |
| **React Router** | 6.x | Client-seitiges Routing |
| **TanStack Query** | 5.x | Server State Management |
| **Zustand** | 5.x | UI State Management |
| **Tailwind CSS** | 4.x | Utility-First Styling |
| **Vite** | 7.x | Build Tool & Dev Server |
| **TypeScript** | 5.x | Type Safety (partial) |
| **Lucide React** | Latest | Icon Library |

## 🎨 Design System

### Farben (Dark Mode)

- **Background:** `slate-900` (#0f172a)
- **Cards:** `slate-800/40` mit Backdrop Blur
- **Primary:** `blue-600` bis `indigo-600` (Gradients)
- **Status:**
  - Healthy: `emerald-500` 🟢
  - Warning: `amber-500` 🟡
  - Critical: `rose-500` 🔴

### Typografie

- **Font:** Inter (Google Fonts)
- **H1:** 2xl, bold
- **Body:** sm, medium weight
- **Metadata:** xs, slate-500

## 🔌 API Struktur (Mock)

Das Frontend nutzt aktuell Mock-Daten aus `src/data/mockApi.ts`:

```typescript
// Services
GET  /api/services              → Liste aller Services
GET  /api/services/:id          → Service Details

// Service-spezifische Ressourcen
GET  /api/services/:id/hosts    → Hosts eines Service
GET  /api/services/:id/networks → Networks eines Service
GET  /api/services/:id/groups   → Groups eines Service
GET  /api/services/:id/policies → Policies eines Service

// Dashboard
GET  /api/dashboard/stats       → Statistiken (Counts, Trends)
GET  /api/dashboard/activity    → Recent Activity Timeline
GET  /api/dashboard/expiring    → Expiring Policies (72h)
```

### Mock-Daten

- **10 Services:** ATREMOTE, AD, MOODLE, SAP, VMW, DMS, EXCHANGE, WEB, DB, BACKUP
- **16 Hosts:** Verteilt über Services (Printer, Server, Device)
- **7 Networks:** CIDR Notation (10.x.x.x/24, 192.168.x.x/24)
- **5 Groups:** Host/Network/Mixed Groups mit Members
- **10 Policies:** Mit Source, Dest, Services (Ports), Action, TTL, Expiration

## 📋 Routing

| Route | Komponente | Beschreibung |
|-------|-----------|--------------|
| `/` | Dashboard | Overview mit Stats & Charts |
| `/services` | ServicesOverview | Grid/List aller Services |
| `/services/:id` | ServiceDetailView | Service Overview Tab |
| `/services/:id/hosts` | ServiceDetailView | Hosts Tab |
| `/services/:id/networks` | ServiceDetailView | Networks Tab |
| `/services/:id/groups` | ServiceDetailView | Groups Tab |
| `/services/:id/policies` | ServiceDetailView | Policies Tab |

## ✅ Implementation Status

### Phase 1 & 2: FERTIG ✅
- Setup, Layout, Design System
- Dashboard mit allen Widgets
- Services Overview (Grid/List)
- Mock Data & API

### Phase 3 & 4: TEILWEISE ✅
- Service Detail View (Read-Only)
- Entity Tabs (Hosts, Networks, Groups, Policies)
- ⏳ CRUD Forms fehlen noch

### Nächste Schritte
1. CRUD Forms (Add/Edit Hosts, Networks, Groups)
2. Policy Management (Create/Edit Multi-Step)
3. Global Views (/global/hosts, etc.)
4. React Flow Topology Visualisierung

## 🐛 Known Issues

- [ ] TypeScript Migration nicht vollständig (Mix aus .js/.ts)
- [ ] Light Mode nicht implementiert (nur Toggle UI)
- [ ] Search Bar (Header) nur UI, nicht funktional
- [ ] Keine Virtualisierung für große Tabellen
- [ ] HeadlessUI noch nicht genutzt (Modals, Dropdowns)

## 📝 Entwickler-Notizen

### State Management

- **UI State (Zustand):**
  - `theme` (dark/light)
  - `sidebarCollapsed` (boolean)
  - `currentServiceId` (number | null)

- **Server State (TanStack Query):**
  - Services, Hosts, Networks, Groups, Policies
  - Dashboard Stats, Activity, Health
  - Caching, Background Refetch, Optimistic Updates

### Custom Hooks

```jsx
// Services
const { data: services } = useServices();
const { data: service } = useServiceById(serviceId);
const { data: hosts } = useServiceHosts(serviceId);

// Dashboard
const { data: stats } = useDashboardStats();
const { data: activity } = useRecentActivity();
const { data: expiring } = useExpiringPolicies();
```

## 🚧 Roadmap

- [ ] **v0.3.0** - CRUD Forms & Policy Management
- [ ] **v0.4.0** - Global Views & Cross-Service Search
- [ ] **v0.5.0** - React Flow Topology Integration
- [ ] **v0.6.0** - Real Backend Integration (REST API)
- [ ] **v1.0.0** - Production Ready (Tests, Docs, Deployment)

## 📄 Lizenz

Siehe Root-Verzeichnis LICENSE Datei

---

**Erstellt am:** 2024-11-29  
**Version:** 0.2.0  
**Status:** In Development (Phase 1 & 2 abgeschlossen)
