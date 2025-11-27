# Technical Stack Recommendation

## Frontend Framework
-   **React**: Already in use. Version 19.x is excellent.
-   **Vite**: Build tool, already in use.

## Diagramming Library
-   **React Flow (@xyflow/react)**: The core library. It provides the canvas, node/edge rendering, and interaction handlers.
    -   *Justification*: Industry standard for React-based node editors, highly customizable, good performance.

## State Management
-   **Zustand**:
    -   *Justification*: Lightweight, easy to use, and works perfectly with React Flow's internal state. It avoids the boilerplate of Redux.

## Styling
-   **Tailwind CSS**:
    -   *Recommendation*: Highly recommended for building the custom node UIs and the sidebar/properties panel quickly and consistently.
    -   *Alternative*: CSS Modules if Tailwind is not desired, but Tailwind is faster for prototyping this kind of UI.

## Layout Engine
-   **Dagre**:
    -   *Status*: Already installed.
    -   *Usage*: Good for simple hierarchical layouts.
-   **Elkjs** (Optional):
    -   *Usage*: Better for complex graphs with nested groups. We can start with Dagre and upgrade if needed.

## Icons
-   **Lucide React**:
    -   *Justification*: Clean, modern icons that fit the "professional" aesthetic.

## Backend Communication
-   **Axios**: Already installed.
-   **React Query (TanStack Query)** (Optional but recommended):
    -   *Justification*: For managing server state (loading rules, caching, optimistic updates).

## Structure
```
src/
  components/
    nodes/
      HostNode.jsx
      NetworkNode.jsx
      GroupNode.jsx
    edges/
      RuleEdge.jsx
    ui/
      Sidebar.jsx
      PropertiesPanel.jsx
  store/
    useStore.js
  utils/
    layout.js
```
