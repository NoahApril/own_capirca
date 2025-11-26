import { useCallback, useEffect, useState } from 'react';
import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    addEdge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import axios from 'axios';

const initialNodes = [];
const initialEdges = [];

function Flow({ policyId = 1 }) {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    const onConnect = useCallback(
        (params) => setEdges((eds) => addEdge(params, eds)),
        [setEdges],
    );

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`/policies/${policyId}/graph`);
                const { nodes: apiNodes, edges: apiEdges } = response.data;

                // Ensure nodes have position if missing (though backend provides it)
                const validNodes = apiNodes.map(node => ({
                    ...node,
                    position: node.position || { x: 0, y: 0 }
                }));

                setNodes(validNodes);
                setEdges(apiEdges);
            } catch (error) {
                console.error("Error fetching graph data:", error);
            }
        };

        fetchData();
    }, [policyId, setNodes, setEdges]);

    return (
        <div style={{ width: '100vw', height: '100vh' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
            >
                <Controls />
                <MiniMap />
                <Background variant="dots" gap={12} size={1} />
            </ReactFlow>
        </div>
    );
}

export default Flow;
