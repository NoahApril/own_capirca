# WebGUI Layout & Design System

Dieses Dokument definiert die visuellen Richtlinien, das Layout-Raster und das CSS-Design-System für das Firewall Management System. Es basiert auf den erstellten Mockups und dem "Service-First"-Ansatz.

## 1. Design-Philosophie

Das Design folgt einem **"Modern Dark Mode"** Ansatz mit **Glassmorphism**-Elementen. Es soll professionell, technisch versiert, aber gleichzeitig zugänglich und modern wirken.

*   **Dominante Ästhetik:** Dunkle Hintergründe, lebendige Akzentfarben (Purple/Blue), Transparenzen, subtile Schatten.
*   **Tiefe:** Nutzung von Layering und z-index, um Hierarchien zu schaffen (Hintergrund -> Content -> Modals/Overlays).
*   **Fokus:** Wichtige Daten (Status, Zahlen) stechen durch Farben hervor; Sekundäres tritt in den Hintergrund.

## 2. Farbpalette (Tailwind Config Basis)

Wir nutzen eine erweiterte Palette basierend auf Tailwind's Default, aber mit spezifischen Anpassungen für den Dark Mode.

### Backgrounds (Dark Theme)
*   `bg-slate-900` (#0f172a): Haupt-Hintergrund der App.
*   `bg-slate-800/50`: Sekundärer Hintergrund für Cards/Panels (mit Backdrop Blur).
*   `bg-slate-950`: Sidebar und Header Hintergrund (dunkler für Kontrast).

### Primary / Accents (Vibrant Gradients)
*   **Primary Blue:** `blue-500` (#3b82f6) bis `indigo-600` (#4f46e5).
*   **Secondary Purple:** `purple-500` (#a855f7) bis `fuchsia-600` (#c026d3).
*   **Gradient Usage:** Buttons, aktive States, wichtige Badges.
    *   *Beispiel:* `bg-gradient-to-r from-blue-600 to-indigo-600`

### Status Colors (Functional)
*   **Success (Healthy/Allow):** `emerald-500` (#10b981) - für "Active", "Allow", "Healthy".
*   **Warning (Expiring/Review):** `amber-500` (#f59e0b) - für "Expiring soon", "Warning".
*   **Error (Critical/Deny):** `rose-500` (#f43f5e) - für "Critical", "Deny", "Error".
*   **Neutral (Inactive):** `slate-500` (#64748b).

### Text Colors
*   `text-slate-50` (Primary): Überschriften, Hauptwerte.
*   `text-slate-300` (Secondary): Labels, Beschreibungen, Tabellen-Inhalte.
*   `text-slate-500` (Muted): Metadaten, Platzhalter.

## 3. Typografie

*   **Font Family:** `Inter` oder `Roboto` (Google Fonts). Modern, gut lesbar bei kleinen Größen (Tabellen).
*   **Hierarchie:**
    *   **H1 (Page Title):** `text-2xl font-bold text-slate-50`
    *   **H2 (Section Title):** `text-lg font-semibold text-slate-200`
    *   **H3 (Card Title):** `text-base font-medium text-slate-300`
    *   **Body:** `text-sm text-slate-300` (Standard für Tabellen und Content)
    *   **Small:** `text-xs text-slate-500` (Metadaten, Footer)

## 4. Layout-Struktur

Das Layout basiert auf einem **CSS Grid / Flexbox** System mit fester Sidebar und Header.

```css
/* App Container */
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #0f172a; /* bg-slate-900 */
}

/* Sidebar */
.sidebar {
  width: 280px;
  flex-shrink: 0;
  background-color: #020617; /* bg-slate-950 */
  border-right: 1px solid rgba(255,255,255, 0.05);
  display: flex;
  flex-direction: column;
}

/* Main Content Wrapper */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* Header */
.header {
  height: 64px;
  background-color: rgba(15, 23, 42, 0.8); /* Glass effect */
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255, 0.05);
  display: flex;
  align-items: center;
  padding: 0 24px;
  z-index: 10;
}

/* Scrollable Content Area */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  scroll-behavior: smooth;
}
```

## 5. Komponenten-Design (CSS & Tailwind)

### Glassmorphism Card
Die Standard-Container für Inhalte (Dashboard-Widgets, Tabellen-Wrapper).

```html
<div class="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-6">
  <!-- Content -->
</div>
```

### Data Tables (Hosts & Policies)
Tabellen müssen bei hoher Datendichte lesbar bleiben.

*   **Header:** `bg-slate-900/50 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-white/5`
*   **Row:** `hover:bg-white/5 transition-colors duration-150 group`
*   **Cell:** `px-6 py-4 whitespace-nowrap text-sm text-slate-300 border-b border-white/5`
*   **Action Icons:** `opacity-0 group-hover:opacity-100 transition-opacity text-slate-400 hover:text-white`

### Badges & Chips
Für Status, Service-Namen, IPs.

*   **Base:** `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium`
*   **Service Badge (Primary):** `bg-indigo-500/10 text-indigo-400 border border-indigo-500/20`
*   **Active/Allow:** `bg-emerald-500/10 text-emerald-400 border border-emerald-500/20`
*   **Warning/Expiring:** `bg-amber-500/10 text-amber-400 border border-amber-500/20`
*   **Critical/Deny:** `bg-rose-500/10 text-rose-400 border border-rose-500/20`

### Buttons
*   **Primary:** `bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-indigo-500/30 rounded-lg px-4 py-2 font-medium transition-all`
*   **Secondary:** `bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 rounded-lg px-4 py-2 transition-all`
*   **Danger:** `bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-lg px-4 py-2`

### Inputs & Search
*   **Style:** `bg-slate-950/50 border border-white/10 rounded-lg text-slate-200 placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all`

## 6. Spezifische Layouts (aus Mockups)

### Dashboard Grid
```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}
```

### Policy Table Layout
Die Policy-Tabelle benötigt spezielle Spaltenbreiten.
*   **Source/Dest:** `min-w-[200px]` (Platz für mehrere Badges/Chips)
*   **Service:** `w-[150px]`
*   **Action:** `w-[100px]`
*   **TTL:** `w-[150px]` (für Progress Bar)

### Service Detail View (Tabs)
*   **Tab Container:** `border-b border-white/10 mb-6`
*   **Tab Item (Active):** `border-b-2 border-indigo-500 text-indigo-400`
*   **Tab Item (Inactive):** `text-slate-400 hover:text-slate-200 hover:border-white/20`

## 7. Animationen

*   **Hover Effects:** `transition-all duration-200 ease-in-out`
*   **Page Transition:** Fade-in beim Wechseln von Routen.
*   **Modal:** Scale-in + Fade-in mit Backdrop Blur.

---
**Zusammenfassung:**
Das Design-System kombiniert die technische Nüchternheit eines Admin-Tools mit der visuellen Attraktivität moderner Consumer-Apps. Der Dark Mode ist nicht nur ästhetisch, sondern schont bei langer Nutzung die Augen. Glassmorphism wird gezielt eingesetzt, um Tiefe und Kontext zu schaffen, ohne vom Inhalt abzulenken.
