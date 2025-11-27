# Implementation Plan: React Flow Firewall Visualizer

## Phase 1: Setup & Infrastructure
1.  **Install Dependencies**:
    -   `npm install zustand lucide-react`
    -   `npm install -D tailwindcss postcss autoprefixer`
    -   `npx tailwindcss init -p`
2.  **Configure Tailwind**:
    -   Update `tailwind.config.js` to include paths to all template files.
    -   Add Tailwind directives to `index.css` (or create it if missing).
3.  **Project Structure**:
    -   Create directories: `src/components/nodes`, `src/components/edges`, `src/components/ui`, `src/store`.

## Phase 2: Core Components
1.  **Custom Nodes** (`src/components/nodes/`):
    -   `HostNode.jsx`: Displays Host icon, name, IP. Handles selection.
    -   `NetworkNode.jsx`: Displays Network icon, name, CIDR.
    -   `GroupNode.jsx`: Container style node.
2.  **UI Components** (`src/components/ui/`):
    -   `Sidebar.jsx`: Contains draggable items for Host, Network, Group.
    -   `PropertiesPanel.jsx`: Displays form fields based on selected element (Node or Edge).
3.  **Store** (`src/store/useStore.js`):
    -   Define Zustand store for `nodes`, `edges`, `selectedId`.
    -   Actions: `addNode`, `updateNode`, `onNodesChange`, `onEdgesChange`, `onConnect`.

## Phase 3: Integration & Logic
1.  **Update Flow.jsx**:
    -   Replace local state with Zustand store hooks.
    -   Register custom node types.
    -   Add `Sidebar` and `PropertiesPanel` to the layout.
    -   Implement `onDrop` handler to create nodes from Sidebar drag.
2.  **Edge Customization**:
    -   Implement `CustomEdge` if needed (e.g., to show rule summary on the line).
    -   Ensure edges are clickable and update the `selectedId` in store.

## Phase 4: Refinement
1.  **Styling**:
    -   Apply "professional" look using Tailwind (shadows, rounded corners, neutral colors).
2.  **Mock Data**:
    -   Create a mock initial state to verify the visualization of a complex topology.

## Verification
-   **Manual Test**:
    -   Drag a Host from sidebar -> Drop on canvas -> Check if node appears.
    -   Select node -> Check if Properties Panel shows details.
    -   Edit name in Panel -> Check if Node updates.
    -   Connect two nodes -> Check if Edge appears.
    -   Select Edge -> Check if Panel shows Rule options.
