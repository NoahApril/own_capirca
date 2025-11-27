import { create } from 'zustand';
import {
    addEdge,
    applyNodeChanges,
    applyEdgeChanges,
} from '@xyflow/react';

const useStore = create((set, get) => ({
    nodes: [],
    edges: [],
    selectedId: null,

    onNodesChange: (changes) => {
        set({
            nodes: applyNodeChanges(changes, get().nodes),
        });
    },

    onEdgesChange: (changes) => {
        set({
            edges: applyEdgeChanges(changes, get().edges),
        });
    },

    onConnect: (connection) => {
        set({
            edges: addEdge({ ...connection, type: 'default', animated: true }, get().edges),
        });
    },

    addNode: (node) => {
        set({
            nodes: [...get().nodes, node],
        });
    },

    updateNode: (id, data) => {
        set({
            nodes: get().nodes.map((node) =>
                node.id === id ? { ...node, data: { ...node.data, ...data } } : node
            ),
        });
    },

    updateEdge: (id, data) => {
        set({
            edges: get().edges.map((edge) =>
                edge.id === id ? { ...edge, data: { ...edge.data, ...data } } : edge
            ),
        });
    },

    deleteNodes: (nodeIds) => {
        const idsToDelete = Array.isArray(nodeIds) ? nodeIds : [nodeIds];

        // Remove nodes
        const newNodes = get().nodes.filter(node => !idsToDelete.includes(node.id));

        // Remove edges connected to deleted nodes
        const newEdges = get().edges.filter(edge =>
            !idsToDelete.includes(edge.source) && !idsToDelete.includes(edge.target)
        );

        set({
            nodes: newNodes,
            edges: newEdges,
            selectedId: null
        });
    },

    setSelectedId: (id) => {
        set({ selectedId: id });

        // Also update selection state in nodes/edges for visual feedback
        set({
            nodes: get().nodes.map((node) => ({
                ...node,
                selected: node.id === id,
            })),
            edges: get().edges.map((edge) => ({
                ...edge,
                selected: edge.id === id,
            })),
        });
    },
}));

export default useStore;
