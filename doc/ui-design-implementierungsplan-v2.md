# UI Design und Implementierungsplan - Service-Orientiertes Firewall Management System

## Überblick

Dieses Dokument beschreibt den Design- und Implementierungsplan für eine moderne, **service-orientierte** React-basierte Benutzeroberfläche zur Verwaltung von Firewall-Regeln. Das System ist um **IT-Services** als zentrale Organisationseinheit strukturiert.

### Problemstellung

**Aktuelle Situation:**
- Alle IT-Services (ATREMOTE, AD, MOODLE, SAP, etc.) mit ihren Hosts, Networks, Groups und Policies werden in einer großen HTML-Datei gespeichert
- Schwer zu navigieren und zu verwalten bei vielen Services und Einträgen
- Keine service-orientierte Organisation
- Keine Suchfunktion, Filterung oder erweiterte Datenverwaltung
- Keine Möglichkeit zur Visualisierung von Beziehungen innerhalb eines Services

**Ziele:**
- **Service-First Architecture**: Services als Top-Level-Organisationseinheit
- Moderne, responsive React-Anwendung mit hervorragender UX
- Jeder Service hat seine eigenen Hosts, Networks, Groups und Policies
- Effiziente Verwaltung großer Datenmengen (Virtualisierung)
- Erweiterte Such-, Filter- und Sortierfunktionen
- Visuelle Darstellung von Beziehungen (React Flow Integration)
- CRUD-Operationen für alle Entitäten
- Export/Import Funktionalität

---

## Konzeptionelles Modell

### Service-Container-Hierarchie

```
┌──────────────────────────────────────┐
│          SERVICE (z.B. ATREMOTE)     │
│  ┌────────────────────────────────┐  │
│  │ Hosts                          │  │
│  │ - host-192.168.10.5            │  │
│  │ - srv-office-app1              │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ Networks                       │  │
│  │ - admin-netzwerk               │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ Groups                         │  │
│  │ - PRINTER-GROUP-01             │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ Policies                       │  │
│  │ - admin-netzwerk →             │  │
│  │   srv-office-app1              │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

**Wichtig**: 
- **Services** sind die Top-Level-Entität (ATREMOTE, AD, MOODLE, SAP, etc.)
- Jeder Service ist ein **Container** für:
  - Hosts (Server, Geräte)
  - Networks (Netzwerke)
  - Groups (Gruppierungen)
  - Policies (Firewall-Regeln)
- Alle Entitäten gehören zu genau einem Service
- Services können über 150+ verschiedene IT-Dienste repräsentieren

---

## Design-Philosophie

### UI/UX Prinzipien

1. **Service-First Approach**
   - Services als primäre Navigation und Organisation
   - Dashboard zeigt Service-Übersicht mit Health Status
   - Service-Detail-Views mit Tabs für Hosts/Networks/Groups/Policies
   - Schnellzugriff auf häufig verwendete Services

2. **Hierarchische Navigation**
   - Breadcrumbs: Services → ATREMOTE → Hosts
   - Kontextbezogene Aktionen (innerhalb eines Services)
   - Service-Switcher für schnellen Wechsel
   - Globale Suche über alle Services

3. **Datenzentrisches Design**
   - Leistungsstarke Tabellen mit erweiterten Funktionen
   - Service-spezifische Filterung
   - Inline-Bearbeitung wo sinnvoll
   - Bulk-Operationen für Effizienz
   - Virtualisierung für große Datensätze

4. **Visuelle Intelligenz**
   - Service Health Indicators
   - React Flow für Service-Topologie
   - Farbcodierung nach Status/Typ
   - Icons für schnelle Erkennung
   - Visuelle Hierarchien

5. **Moderne Ästhetik**
   - Glassmorphism-Effekte
   - Smooth Animations und Transitions
   - Dark Mode Support
   - Responsive Design (Desktop-first, aber mobile-ready)

---

## User Interface Design

### 1. Layout-Struktur

```
┌─────────────────────────────────────────────────────────────┐
│  Header / Navigation                      🔍 Search  👤 User │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│ Sidebar  │              Main Content Area                   │
│          │                                                   │
│ 📊 Dashbrd│         (Dynamic Content basierend auf          │
│ 🏢 Services│          ausgewähltem Menüpunkt)               │
│   > Active │                                                 │
│   > All    │                                                 │
│ ────────  │                                                  │
│ 🌐 Global │                                                  │
│   - Hosts │                                                  │
│   - Netwrks│                                                 │
│   - Groups│                                                  │
│   - Polics│                                                  │
│          │                                                   │
└──────────┴─────────────────────────────────────────────────┘
```

### 2. Dashboard View (Service-Oriented)

**Komponenten:**

- **Statistik-Karten** (5er-Grid)
  - Anzahl Services (mit Trend-Indikator)
  - Anzahl Hosts gesamt (mit Trend-Indikator)
  - Anzahl Networks gesamt (mit Trend-Indikator)
  - Anzahl Groups gesamt (mit Trend-Indikator)
  - Anzahl Policies gesamt (mit Status-Breakdown)

- **Services at a Glance** (Prominente Sektion)
  - Service Health Status (Pie Chart: Healthy, Warning, Critical)
  - Top 5 Services by Resource Count (Bar Chart)
  - Services Requiring Attention (List mit Warnungen)

- **Quick Actions Panel**
  - Schnell Service hinzufügen
  - Service-Templates (vordefinierte Service-Typen)
  - Schnell Policy erstellen
  - Export/Import

- **Recent Activity Timeline**
  - Letzte Änderungen chronologisch (service-übergreifend)
  - Filter nach Service und Typ
  - Drill-down zu Service-Details

- **Policy Expiration by Service**
  - Chart zeigt bald ablaufende Policies pro Service
  - Warnungen für kritische Services

**Visualisierung:**
```
┌──────────────────────────────────────────────────────────┐
│  Dashboard                                               │
├──────────────────────────────────────────────────────────┤
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│ │Services│ │  Hosts │ │Networks│ │ Groups │ │Policies│ │
│ │  158   │ │ 1,250  │ │  340   │ │  480   │ │ 5,230  │ │
│ │ ↗ +5   │ │ ↗ +23  │ │ ↘ -2   │ │ ↗ +8   │ │ ↗ +67  │ │
│ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │
│                                                           │
│ ┌─ Services at a Glance ─────────────────────────────┐  │
│ │ ┌─ Health ─┐  ┌─ Top 5 Services ──────────────┐   │  │
│ │ │🟢 85%     │  │ ATREMOTE    ████████░ 450     │   │  │
│ │ │🟡 12%     │  │ AD          ███████░░ 380     │   │  │
│ │ │🔴  3%     │  │ MOODLE      ██████░░░ 320     │   │  │
│ │ └───────────┘  │ SAP         █████░░░░ 270     │   │  │
│ │                │ VMW         ████░░░░░ 210     │   │  │
│ │                └───────────────────────────────┘   │  │
│ │ ⚠️  Services Requiring Attention:                  │  │
│ │   • ATREMOTE: 5 policies expiring in 24h          │  │
│ │   • DMS: Network connectivity issues              │  │
│ └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 3. Services Overview

**Features:**
- **Header Section**
  - Titel "Services" + Anzahl
  - Suchfeld (mit Debouncing)
  - Filter-Buttons (By Status: Active/Warning/Critical, By Category)
  - "Neu erstellen" Button (Primary Action)
  - Export-Button (CSV, JSON)

- **View Options**
  - Grid View (Default): Service-Karten
  - List View: Kompakte Tabelle
  - Category View: Gruppiert nach Kategorie

- **Service Cards (Grid View)**
  - Service-Kurzname als Badge (z.B. "ATREMOTE")
  - Vollständiger Name (z.B. "Ricoh @Remote")
  - Status-Indikator (Grün/Gelb/Rot)
  - Quick Stats: "5 Hosts | 3 Networks | 2 Groups | 12 Policies"
  - Warning Icons bei expiring policies
  - Hover: Quick Actions (View, Edit, Settings)
  - Farbliche Kodierung nach Status

**Visualisierung:**
```
┌──────────────────────────────────────────────────────────┐
│ Services (158)        🔍 Search    [Filter] [+ New]      │
├──────────────────────────────────────────────────────────┤
│ ┌─ ATREMOTE ───────┐ ┌─ AD ──────────┐ ┌─ MOODLE ────┐ │
│ │🟢 Ricoh @Remote  │ │🟢 Active Dir  │ │🟡 E-Learning│ │
│ │ 5 Hosts          │ │ 23 Hosts      │ │ 8 Hosts     │ │
│ │ 3 Networks       │ │ 12 Networks   │ │ 4 Networks  │ │
│ │ 2 Groups         │ │ 8 Groups      │ │ 3 Groups    │ │
│ │ 12 Policies  ⚠️  │ │ 45 Policies   │ │ 28 Policies │ │
│ └──────────────────┘ └───────────────┘ └─────────────┘ │
│ ┌─ SAP ───────────┐ ┌─ VMW ─────────┐ ┌─ DMS ───────┐ │
│ │🟢 SAP System     │ │🟢 VMware      │ │🔴 Document  │ │
│ │ ...              │ │ ...           │ │ Management  │ │
│ └──────────────────┘ └───────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### 4. Service Detail View

**Struktur:**
- **Header**
  - Service Badge + Name
  - Status Indicator
  - Action Buttons (Edit Service, Settings, Delete, Export)
  - Breadcrumb: Services → ATREMOTE

- **Stats Bar** (4 Karten)
  - Hosts: 2
  - Networks: 1
  - Groups: 1
  - Policies: 3

- **Tabbed Interface**
  - **Overview Tab**
    - Service Information (Description, Owner, Created, Firewall)
    - Network Topology Visualization (React Flow)
    - Recent Changes Timeline
    - Quick Actions
    - Policy Expiration Warnings
  
  - **Hosts Tab**
    - Hosts-Tabelle (nur für diesen Service)
    - Add/Remove Hosts
    - Inline-Bearbeitung
  
  - **Networks Tab**
    - Networks-Tabelle (nur für diesen Service)
    - Add/Remove Networks
  
  - **Groups Tab**
    - Groups-Tabelle (nur für diesen Service)
    - Add/Remove Groups
    - Members Management
  
  - **Policies Tab**
    - Policies-Tabelle (nur für diesen Service)
    - Multi-View Toggle (Table/Graph/Card)
    - Create Policy
  
  - **Activity Tab**
    - Service-spezifische Activity Timeline
    - Filter nach Entitätstyp

**Visualisierung:**
```
┌──────────────────────────────────────────────────────────┐
│ Services > ATREMOTE                                      │
├──────────────────────────────────────────────────────────┤
│ 🟢 ATREMOTE - Ricoh @Remote      [Edit] [⚙️] [Delete]   │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                         │
│ │Hosts│ │Netwk│ │Grps │ │Polcy│                         │
│ │  2  │ │  1  │ │  1  │ │  3  │                         │
│ └─────┘ └─────┘ └─────┘ └─────┘                         │
│                                                           │
│ [Overview] [Hosts] [Networks] [Groups] [Policies] [Act] │
├──────────────────────────────────────────────────────────┤
│ Overview Tab Selected:                                   │
│ ┌─ Service Information ──────────────────────────────┐  │
│ │ Description: Ricoh @Remote Druckgeräte             │  │
│ │ Owner: IT Department                               │  │
│ │ Firewall: fw-central-01                            │  │
│ │ Created: 2024-01-15                                │  │
│ └────────────────────────────────────────────────────┘  │
│ ┌─ Network Topology ─────────┐ ┌─ Quick Actions ─────┐ │
│ │ [React Flow Visualisierung]│ │ + Add Host          │ │
│ │                            │ │ + Add Network       │ │
│ │                            │ │ + Create Policy     │ │
│ └────────────────────────────┘ └─────────────────────┘ │
│ ⚠️  Policy Expiration Alert: 5 policies expire in 24h  │
└──────────────────────────────────────────────────────────┘
```

### 5. Service-Specific Entity Views

**Hosts Tab (innerhalb Service-Detail):**
```
Breadcrumb: Services > ATREMOTE > Hosts

ATREMOTE Hosts (2)     🔍 Search    [+ Add Host]

╔═══════════════════════════════════════════════════════════╗
║ ☐ | Name              | IP          | Type    | Comment  ║
╠═══════════════════════════════════════════════════════════╣
║ ☐ | host-192.168.10.5 | 192.168.10.5| Printer | Standort A║
║ ☐ | srv-office-app1   | 203.0.113.45| Server  | Remote App║
╚═══════════════════════════════════════════════════════════╝
```

**Tabellen-Spalten:**

**Hosts (Service-spezifisch):**
| Name | IP-Adresse | Type | Comment | Used in Policies | Aktionen |

**Networks (Service-spezifisch):**
| Name | IP-Adresse/CIDR | Comment | Used in Policies | Aktionen |

**Groups (Service-spezifisch):**
| Name | Type | Mitglieder (Count) | Comment | Aktionen |

**Policies (Service-spezifisch):**
| Quelle | Ziel | Services (Ports) | Aktion | TTL | Counter | Comment | Aktionen |

### 6. Global Views (Service-übergreifend)

Neben der service-spezifischen Navigation gibt es auch **globale Ansichten**:

- **Global > Hosts**: Alle Hosts über alle Services
  - Zusätzliche Spalte: "Service" (Badge mit Service-Name)
  - Filter by Service
  - Klick auf Service-Badge → springt zur Service-Detail-View

- **Global > Networks**: Alle Networks über alle Services
- **Global > Groups**: Alle Groups über alle Services
- **Global > Policies**: Alle Policies über alle Services

**Nutzen**: Für service-übergreifende Analysen, Suchen und Bulk-Operationen

### 7. Create/Edit Forms

**Create Service Form:**
1. **Basic Information**
   - Service-Kurzname (z.B. "ATREMOTE") - Alphanumerisch, Großbuchstaben
   - Vollständiger Name (z.B. "Ricoh @Remote")
   - Description/Kategorie
   - Firewall Assignment (fw-central-01, etc.)
   - Owner/Contact

2. **Initial Setup (Optional)**
   - Template auswählen (vordefinierte Service-Typen)
   - Initial Hosts hinzufügen
   - Initial Networks hinzufügen

**Create Host/Network/Group/Policy Forms:**
- **Service-Kontext beibehalten**: Wenn aus Service-Detail erstellt, automatisch diesem Service zugeordnet
- Ansonsten: Service-Dropdown zur Auswahl
- Rest wie vorher beschrieben

**Policy Form (Multi-Step, service-aware):**
1. **Service & Basis-Info**
   - Service auswählen (oder bereits gesetzt)
   - Kommentar

2. **Quelle & Ziel**
   - Autocomplete gefiltert nach Service
   - Oder service-übergreifende Auswahl

3. **Dienste (Ports) & Aktion**
   - Service-Auswahl (HTTPS=443, SSH=22, Custom)
   - Aktion: erlauben/blockieren
   - TTL

4. **Review & Submit**

---

## Technische Architektur

### Datenmodell

```typescript
// Service ist die Top-Level-Entität
interface Service {
  id: number;
  shortName: string;           // "ATREMOTE"
  fullName: string;            // "Ricoh @Remote"
  description?: string;
  category?: string;           // "Printing", "Infrastructure", etc.
  firewall: string;            // "fw-central-01"
  owner?: string;
  status: 'healthy' | 'warning' | 'critical';
  createdAt: string;
  updatedAt: string;
  
  // Aggregated counts (computed)
  hostsCount: number;
  networksCount: number;
  groupsCount: number;
  policiesCount: number;
  policiesExpiringCount: number;
}

// Alle anderen Entitäten haben serviceId
interface Host {
  id: number;
  serviceId: number;          // FK zu Service
  serviceName: string;        // Für Display (denormalisiert)
  name: string;
  ipAddress: string;
  type?: string;              // "Server", "Printer", "Device"
  comment?: string;
  createdAt: string;
  updatedAt: string;
  usedInPoliciesCount: number; // Computed
}

interface Network {
  id: number;
  serviceId: number;
  serviceName: string;
  name: string;
  ipAddress: string;          // CIDR: "10.10.20.0/24"
  comment?: string;
  createdAt: string;
  updatedAt: string;
  usedInPoliciesCount: number;
}

interface GroupMember {
  type: 'host' | 'network' | 'group';
  id: number;
  name: string;
}

interface Group {
  id: number;
  serviceId: number;
  serviceName: string;
  name: string;
  type: 'host' | 'network' | 'mixed';
  members: GroupMember[];
  comment?: string;
  createdAt: string;
  updatedAt: string;
}

interface Policy {
  id: number;
  serviceId: number;
  serviceName: string;
  source: string[];          // Namen von Hosts/Networks/Groups
  destination: string[];
  services: PortService[];   // Port-basierte Services
  action: 'allow' | 'deny';
  ttlHours: number;
  comment?: string;
  counter: number;
  createdAt: string;
  updatedAt: string;
  expiresAt?: string;
}

// Port-basierte Services (HTTPS, SSH, etc.)
interface PortService {
  name: string;              // "HTTPS", "SSH", "Custom"
  protocol: 'TCP' | 'UDP' | 'ICMP';
  port?: number;             // 443, 22
  portRange?: string;        // "8080-8090"
}

interface ServiceTopology {
  serviceId: number;
  nodes: PolicyGraphNode[];
  edges: PolicyGraphEdge[];
}

interface DashboardStats {
  servicesCount: number;
  servicesHealthy: number;
  servicesWarning: number;
  servicesCritical: number;
  hostsCount: number;
  hostsChange: number;
  networksCount: number;
  networksChange: number;
  groupsCount: number;
  groupsChange: number;
  policiesCount: number;
  policiesAllowCount: number;
  policiesDenyCount: number;
  topServices: {
    serviceId: number;
    serviceName: string;
    resourceCount: number;
  }[];
}

interface ActivityItem {
  id: number;
  serviceId: number;
  serviceName: string;
  type: 'host' | 'network' | 'group' | 'policy' | 'service';
  action: 'created' | 'updated' | 'deleted';
  entityName: string;
  timestamp: string;
  user?: string;
}
```

### Component Tree (aktualisiert)

```
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── ServiceSwitcher (Quick Access)
│   │   ├── GlobalSearch
│   │   └── UserMenu
│   ├── Sidebar
│   │   └── Navigation
│   │       ├── Dashboard
│   │       ├── Services
│   │       │   ├── Active Services
│   │       │   └── All Services
│   │       └── Global Views
│   │           ├── All Hosts
│   │           ├── All Networks
│   │           ├── All Groups
│   │           └── All Policies
│   └── MainContent
│       └── Router
│           ├── Dashboard
│           │   ├── ServiceHealthOverview
│           │   ├── StatsCards
│           │   ├── TopServicesChart
│           │   ├── RecentActivity
│           │   └── ExpirationAlerts
│           ├── ServicesOverview
│           │   ├── PageHeader
│           │   ├── ViewToggle (Grid/List)
│           │   ├── ServiceGrid
│           │   └── ServiceTable
│           ├── ServiceDetailView
│           │   ├── ServiceHeader
│           │   ├── ServiceStatsBar
│           │   └── TabView
│           │       ├── OverviewTab
│           │       │   ├── ServiceInfo
│           │       │   ├── TopologyView (React Flow)
│           │       │   └── QuickActions
│           │       ├── HostsTab
│           │       │   ├── PageHeader
│           │       │   └── ServiceHostsTable
│           │       ├── NetworksTab
│           │       ├── GroupsTab
│           │       └── PoliciesTab
│           │           ├── ViewToggle
│           │           ├── TableView
│           │           └── GraphView
│           ├── GlobalHostsView
│           ├── GlobalNetworksView
│           ├── GlobalGroupsView
│           └── GlobalPoliciesView
└── Shared Components
    ├── ServiceBadge
    ├── StatusIndicator
    ├── Button
    ├── DataTable
    ├── SearchInput
    ├── FilterBar
    ├── ...
```

### Routing (aktualisiert)

**React Router v6**

```
/                                  → Dashboard
/services                          → Services Overview (Grid/List)
/services/new                      → Create Service
/services/:serviceId               → Service Detail (Overview Tab)
/services/:serviceId/hosts         → Service Hosts Tab
/services/:serviceId/hosts/new     → Create Host for Service
/services/:serviceId/networks      → Service Networks Tab
/services/:serviceId/networks/new  → Create Network for Service
/services/:serviceId/groups        → Service Groups Tab
/services/:serviceId/groups/new    → Create Group for Service
/services/:serviceId/policies      → Service Policies Tab
/services/:serviceId/policies/new  → Create Policy for Service
/services/:serviceId/policies/:id/graph → Policy Graph View
/services/:serviceId/activity      → Service Activity Tab
/services/:serviceId/edit          → Edit Service

# Global Views (service-übergreifend)
/global/hosts                      → All Hosts
/global/networks                   → All Networks
/global/groups                     → All Groups
/global/policies                   → All Policies
```

### State Management

**Zustand + React Query**

```typescript
// Zustand Store
interface UIStore {
  theme: 'light' | 'dark';
  sidebarCollapsed: boolean;
  currentServiceId: number | null;
  toggleTheme: () => void;
  toggleSidebar: () => void;
  setCurrentService: (id: number) => void;
}

// React Query Keys (service-aware)
const queryKeys = {
  services: ['services'],
  serviceById: (id: number) => ['services', id],
  serviceHosts: (serviceId: number) => ['services', serviceId, 'hosts'],
  serviceNetworks: (serviceId: number) => ['services', serviceId, 'networks'],
  serviceGroups: (serviceId: number) => ['services', serviceId, 'groups'],
  servicePolicies: (serviceId: number) => ['services', serviceId, 'policies'],
  serviceTopology: (serviceId: number) => ['services', serviceId, 'topology'],
  
  // Global
  allHosts: ['hosts'],
  allNetworks: ['networks'],
  allGroups: ['groups'],
  allPolicies: ['policies'],
  
  dashboard: ['dashboard', 'stats'],
};
```

---

## API Design (aktualisiert)

### REST Endpoints

**Services**
```
GET    /api/services                    → Liste aller Services
GET    /api/services/:id                → Einzelner Service
POST   /api/services                    → Service erstellen
PUT    /api/services/:id                → Service aktualisieren
DELETE /api/services/:id                → Service löschen
GET    /api/services/search?q=...       → Services suchen
GET    /api/services/:id/stats          → Service-Statistiken
GET    /api/services/:id/topology       → Service-Topologie (React Flow)
```

**Hosts (service-spezifisch)**
```
GET    /api/services/:serviceId/hosts        → Hosts eines Services
GET    /api/services/:serviceId/hosts/:id    → Einzelner Host
POST   /api/services/:serviceId/hosts        → Host erstellen
PUT    /api/hosts/:id                        → Host aktualisieren
DELETE /api/hosts/:id                        → Host löschen

# Global
GET    /api/hosts                            → Alle Hosts (service-übergreifend)
GET    /api/hosts/search?q=...               → Hosts suchen
```

**Networks (service-spezifisch)**
```
GET    /api/services/:serviceId/networks
GET    /api/services/:serviceId/networks/:id
POST   /api/services/:serviceId/networks
PUT    /api/networks/:id
DELETE /api/networks/:id

# Global
GET    /api/networks
```

**Groups (service-spezifisch)**
```
GET    /api/services/:serviceId/groups
GET    /api/services/:serviceId/groups/:id
POST   /api/services/:serviceId/groups
PUT    /api/groups/:id
DELETE /api/groups/:id
GET    /api/groups/:id/members

# Global
GET    /api/groups
```

**Policies (service-spezifisch)**
```
GET    /api/services/:serviceId/policies
GET    /api/services/:serviceId/policies/:id
POST   /api/services/:serviceId/policies
PUT    /api/policies/:id
DELETE /api/policies/:id
GET    /api/policies/:id/graph
GET    /api/services/:serviceId/policies/expiring

# Global
GET    /api/policies
GET    /api/policies/expiring
```

**Dashboard**
```
GET    /api/dashboard/stats            → Service-orientierte Statistiken
GET    /api/dashboard/activity         → Recent Activity
GET    /api/dashboard/service-health   → Service Health Overview
```

---

## Implementierungsphasen (aktualisiert)

### Phase 1: Setup & Service-Grundstruktur (3-4 Tage)

**Tasks:**
- [ ] Projekt-Setup mit Service-orientierter Architektur
  - Vite + React + TypeScript
  - Routing mit Service-Hierarchie
  - State Management (Zustand + React Query)
  - Tailwind CSS
  
- [ ] Layout-Komponenten
  - Header mit ServiceSwitcher
  - Sidebar mit Service-Navigation
  - Breadcrumb-Komponente
  - MainContent Wrapper

- [ ] Design System Grundlagen
  - ServiceBadge-Komponente
  - StatusIndicator-Komponente
  - Standard UI Components

- [ ] Mock API (Service-orientiert)
  - Mock-Daten für 10-15 Services (ATREMOTE, AD, MOODLE, etc.)
  - Hierarchische Daten (Service → Hosts/Networks/Groups/Policies)

**Deliverables:**
- Service-orientierte Navigation funktioniert
- Mock API mit hierarchischen Daten

### Phase 2: Dashboard & Services Overview (3-4 Tage)

**Tasks:**
- [ ] Dashboard
  - Service-Health-Overview
  - StatsCards mit Service-Count
  - TopServicesChart
  - ExpirationAlerts by Service

- [ ] Services Overview
  - Service Grid View
  - Service List View
  - Service Cards mit Stats
  - Search & Filter

- [ ] API Integration
  - `/api/services`
  - `/api/dashboard/stats`
  - `/api/dashboard/service-health`

**Deliverables:**
- Funktionierendes Dashboard
- Services Overview mit Grid/List View

### Phase 3: Service Detail View - Overview & Navigation (3-4 Tage)

**Tasks:**
- [ ] Service Detail Layout
  - ServiceHeader
  - ServiceStatsBar
  - TabView-Komponente

- [ ] Overview Tab
  - Service Information Card
  - Topology View (React Flow) - Basic
  - QuickActions Panel
  - Expiration Warnings

- [ ] Navigation & Breadcrumbs
  - Service-Context Management
  - Tab-Switching
  - URL-basierte Navigation

**Deliverables:**
- Service Detail View mit Overview Tab
- Context-aware Navigation

### Phase 4: Service-Specific Entity Views (5-6 Tage)

**Tasks:**
- [ ] Hosts Tab (service-spezifisch)
  - ServiceHostsTable
  - Add/Create Host Forms
  - Service-Filter

- [ ] Networks Tab (service-spezifisch)
  - ServiceNetworksTable
  - Add/Create Network Forms

- [ ] Groups Tab (service-spezifisch)
  - ServiceGroupsTable
  - Members Management (service-aware)

- [ ] API Integration
  - `/api/services/:serviceId/hosts`
  - `/api/services/:serviceId/networks`
  - `/api/services/:serviceId/groups`
  - CRUD-Operationen

**Deliverables:**
- Alle service-spezifischen Entity Tabs funktional
- CRUD für Hosts/Networks/Groups innerhalb eines Services

### Phase 5: Service-Specific Policies View (4-5 Tage)

**Tasks:**
- [ ] Policies Tab (service-spezifisch)
  - ServicePoliciesTable
  - Multi-View Toggle
  - Erweiterte Filter

- [ ] Create Policy Form (service-aware)
  - Multi-Step
  - Service-Context
  - Port-Services Auswahl

- [ ] Edit Policy

- [ ] API Integration
  - `/api/services/:serviceId/policies`
  - CRUD für Policies

**Deliverables:**
- Policies Tab vollständig funktional
- Service-aware Policy CRUD

### Phase 6: Global Views (3-4 Tage)

**Tasks:**
- [ ] Global Hosts View
  - Alle Hosts über alle Services
  - Service-Spalte + Filter
  - Jump to Service

- [ ] Global Networks View
- [ ] Global Groups View
- [ ] Global Policies View

- [ ] Service-Link Komponente
  - Klick auf Service-Badge → Service Detail

**Deliverables:**
- Service-übergreifende Views funktional
- Navigation zwischen Global und Service Views

### Phase 7: Service Topology & Visualisierung (4-5 Tage)

**Tasks:**
- [ ] Service Topology (React Flow)
  - Custom Nodes (Hosts, Networks, Groups)
  - Custom Edges (Policies)
  - Auto-Layout für Service
  - Interaktivität

- [ ] Policy Graph View (innerhalb Service)
  - Graph-basierte Policy-Darstellung

- [ ] Backend Support
  - `/api/services/:id/topology`
  - Algorithmus für Topologie-Generierung

**Deliverables:**
- Visual Service Topology
- Interactive Policy Graphs

### Phase 8: Service Management & CRUD (2-3 Tage)

**Tasks:**
- [ ] Create Service Form
  - Basic Info
  - Template-Auswahl (optional)
  - Initial Setup

- [ ] Edit Service Form
- [ ] Delete Service (mit Warnungen)
- [ ] Service Templates
  - Vordefinierte Service-Typen
  - Auto-Setup von Hosts/Networks

**Deliverables:**
- Service CRUD vollständig
- Templates funktional

### Phase 9: Polish & Advanced Features (4-5 Tage)

**Tasks:**
- [ ] Service Health Monitoring
  - Auto-Update von Status
  - Health Checks
  - Notifications

- [ ] Service-Switcher (Quick Access)
  - Dropdown im Header
  - Recent Services
  - Favorites

- [ ] Dark Mode
- [ ] Animations & Transitions
- [ ] Error Handling
- [ ] Export/Import (service-basiert)
- [ ] Bulk Operations
- [ ] Performance Optimierung

**Deliverables:**
- Polierte, produktionsreife UI
- Alle erweiterten Features

### Phase 10: Testing & Dokumentation (3-4 Tage)

**Tasks:**
- [ ] Unit Tests (service-aware)
- [ ] Integration Tests
- [ ] Documentation
- [ ] Deployment

**Deliverables:**
- Getestete Anwendung
- Deployment-ready

---

## Geschätzte Zeitrahmen (aktualisiert)

| Phase | Beschreibung | Zeitaufwand |
|-------|--------------|-------------|
| 1 | Setup & Service-Grundstruktur | 3-4 Tage |
| 2 | Dashboard & Services Overview | 3-4 Tage |
| 3 | Service Detail View | 3-4 Tage |
| 4 | Service-Specific Entity Views | 5-6 Tage |
| 5 | Service-Specific Policies | 4-5 Tage |
| 6 | Global Views | 3-4 Tage |
| 7 | Service Topology | 4-5 Tage |
| 8 | Service Management | 2-3 Tage |
| 9 | Polish & Advanced Features | 4-5 Tage |
| 10 | Testing & Dokumentation | 3-4 Tage |
| **Gesamt** | | **34-48 Tage** |

---

## Verzeichnisstruktur (aktualisiert)

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── ServiceBadge.tsx
│   │   │   ├── StatusIndicator.tsx
│   │   │   ├── Button.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── ServiceSwitcher.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Breadcrumb.tsx
│   │   │   └── ...
│   │   ├── dashboard/
│   │   │   ├── ServiceHealthOverview.tsx
│   │   │   ├── TopServicesChart.tsx
│   │   │   ├── ExpirationAlerts.tsx
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── ServicesGrid.tsx
│   │   │   ├── ServiceCard.tsx
│   │   │   ├── ServiceDetailView.tsx
│   │   │   ├── ServiceHeader.tsx
│   │   │   ├── ServiceStatsBar.tsx
│   │   │   └── tabs/
│   │   │       ├── OverviewTab.tsx
│   │   │       ├── HostsTab.tsx
│   │   │       ├── NetworksTab.tsx
│   │   │       ├── GroupsTab.tsx
│   │   │       ├── PoliciesTab.tsx
│   │   │       └── ActivityTab.tsx
│   │   ├── hosts/
│   │   │   ├── HostsTable.tsx
│   │   │   ├── ServiceHostsTable.tsx  # Service-aware
│   │   │   ├── HostForm.tsx
│   │   │   └── ...
│   │   ├── networks/
│   │   ├── groups/
│   │   ├── policies/
│   │   │   ├── PoliciesTable.tsx
│   │   │   ├── ServicePoliciesTable.tsx
│   │   │   ├── PolicyForm.tsx
│   │   │   └── ...
│   │   └── topology/
│   │       ├── ServiceTopology.tsx
│   │       └── PolicyGraph.tsx
│   ├── hooks/
│   │   ├── useServices.ts
│   │   ├── useServiceHosts.ts
│   │   ├── useServiceNetworks.ts
│   │   ├── useServicePolicies.ts
│   │   ├── useGlobalHosts.ts
│   │   └── ...
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── ServicesOverview.tsx
│   │   ├── ServiceDetailView.tsx
│   │   ├── GlobalHostsView.tsx
│   │   ├── GlobalNetworksView.tsx
│   │   └── ...
│   ├── types/
│   │   └── index.ts
│   └── ...
```

---

## Technologie-Stack

**Unverändert**:
- React 18+ mit TypeScript
- Vite
- React Router v6
- Zustand + TanStack Query
- Tailwind CSS + HeadlessUI
- React Flow
- Axios

---

## Wichtige Design-Entscheidungen

> [!IMPORTANT]
> **Service-Orientierung ist fundamental**
> 
> - Services sind die primäre Organisationseinheit
> - Jede Entität (Host, Network, Group, Policy) gehört zu einem Service
> - UI-Navigation spiegelt diese Hierarchie wider
> - Breadcrumbs zeigen Service-Kontext
> - Datenbank-Schema muss `serviceId` Foreign Key in allen Tabellen haben

> [!WARNING]
> **Daten-Migration**
> 
> - Bestehende HTML-Daten müssen in Service-Struktur migriert werden
> - Services müssen identifiziert und kategorisiert werden
> - Zuordnung von Hosts/Networks/Groups/Policies zu Services

> [!IMPORTANT]
> **Backend-Entwicklung**
> 
> - REST API muss service-aware sein
> - Nested Routes für service-spezifische Ressourcen
> - Global Routes für service-übergreifende Views
> - Service Health Monitoring (optional, aber empfohlen)

---

## Nächste Schritte

1. ✅ **Service-Konzept validiert** ← FERTIG
2. ⏳ **Backend-API mit Service-Support spezifizieren**
3. ⏳ **Mock-Daten mit Service-Hierarchie erstellen**
4. ⏳ **Implementierung starten (Phase 1)**

---

**Erstellt von**: Antigravity AI Assistant  
**Datum**: 2025-11-29  
**Version**: 2.0 (Service-Oriented)  
**Projekt**: Capirca Firewall Management
