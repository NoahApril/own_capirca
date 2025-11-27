# Concept Design: Visual Firewall Rule Editor

## Overview
The goal is to create a visual editor for firewall rules using React Flow. This system will allow users to define network topologies and firewall rules by dragging and dropping components (Hosts, Networks, Groups) and connecting them with edges that represent the rules. The interface will be inspired by tools like N8N or Dify, offering a professional and intuitive user experience.

## Core Features

### 1. Visual Canvas
-   **Interactive Workspace**: A zoomable and pannable canvas where users can place and arrange nodes.
-   **Grid/Background**: Visual aids (dots/lines) to help with alignment.
-   **MiniMap**: For easy navigation of large diagrams.
-   **Controls**: Zoom in/out, fit view, lock.

### 2. Node Types (Components)
We will define custom node types for different network entities:
-   **Host Node**: Represents a single IP address or hostname.
    -   *Visual*: Icon + Name + IP.
    -   *Handles*: Input/Output for connections.
-   **Network Node**: Represents a subnet (CIDR).
    -   *Visual*: Icon + Name + CIDR.
-   **Group Node**: Represents a collection of Hosts or Networks.
    -   *Visual*: Container-like look or distinct icon.
    -   *Expandable*: Option to expand and show child elements (Hosts/Networks) within the group to visualize the full topology.
-   **Service/Port Node** (Optional but recommended): To define specific ports/protocols if not part of the edge.

### 3. Edges (Firewall Rules)
Connections between nodes represent the flow of traffic or the application of a rule.
-   **Directional Edges**: Source -> Destination.
-   **Edge Labels**: Show protocol/port summary (e.g., "TCP 80").
-   **Interactive**: Click to edit rule details.

### 4. Sidebar / Drag-and-Drop Menu
-   **Component Palette**: List of available node types (Host, Network, Group) to drag onto the canvas.
-   **Search**: Filter components by name.

### 5. Properties Panel (Contextual Sidebar)
-   **Selection-based**: When a node or edge is selected, this panel shows its details.
-   **Node Editing**: Edit Name, IP, CIDR, Group Members.
-   **Rule Editing**: When an edge is selected, edit:
    -   Action (Allow/Deny)
    -   Protocol (TCP/UDP/ICMP)
    -   Ports (Source/Dest)
    -   Logging options
    -   Comments

### 6. CRUD & State Management
-   **Create**: Drag new nodes, draw new edges.
-   **Read**: Load existing topology/rules from backend.
-   **Update**: Edit properties, move nodes, reconnect edges.
-   **Delete**: Remove nodes/edges.
-   **Validation**: Real-time validation (e.g., valid IP, non-cyclic groups if applicable).

## User Interaction Flow
1.  **Setup**: User opens the editor. Existing rules are loaded and visualized.
2.  **Add Entity**: User drags a component (Host, Network, or Group) from the sidebar to the canvas.
3.  **Configure Entity**: User clicks the new node. Properties panel opens.
    -   **Lookup**: Instead of typing a name/IP, the user searches and selects an existing object (Host, Network, or Group) from a dropdown/lookup list.
    -   **Display**: The node automatically populates with the details (Name, IP, CIDR, Members) of the selected object.
4.  **Define Rule**: User drags a connection from a Source Node (Host/Network/Group) to a Destination Node (Host/Network/Group).
5.  **Configure Rule**: User clicks the connection line. Properties panel shows Rule details.
    -   **Action**: Select from a predefined list of actions (e.g., Allow, Deny, Reject) defined in the policy.
    -   **Service/Protocol**:
        -   **Service Lookup**: Select a predefined Service Object (e.g., "HTTP", "SSH") from a dropdown. This automatically sets the Protocol (e.g., TCP) and Ports (e.g., 80, 443).
        -   **Custom Definition**: If no service object matches, manually select Protocol (TCP/UDP/ICMP) and enter Ports.
6.  **Save**: User clicks "Save". The graph is serialized and sent to the backend.

## Visual Style
-   **Modern UI**: Clean lines, rounded corners, subtle shadows (Glassmorphism where appropriate).
-   **Color Coding**:
    -   Hosts: Blue
    -   Networks: Green
    -   Groups: Purple
    -   Allow Rules: Green edges
    -   Deny Rules: Red edges

## Layouting
-   **Auto-Layout**: Button to automatically arrange nodes using a layout algorithm (Dagre or Elkjs) to untangle the graph.
