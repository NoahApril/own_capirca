import { useCallback, useEffect, useRef, useState } from 'react';
import {
    ReactFlow,
    MiniMap,
    Controls,
    Background,
    useReactFlow,
    ReactFlowProvider,
    Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import axios from 'axios';

import useStore from './store/useFlowStore';
import HostNode from './components/nodes/HostNode';
import NetworkNode from './components/nodes/NetworkNode';
import GroupNode from './components/nodes/GroupNode';
import Sidebar from './components/flow_ui/Sidebar';
import PropertiesPanel from './components/flow_ui/PropertiesPanel';
import DeleteConfirmDialog from './components/flow_ui/DeleteConfirmDialog';

const nodeTypes = {
    host: HostNode,
    network: NetworkNode,
    net_group: GroupNode,

};

function FlowContent({ policyId = 1 }) {
    const reactFlowWrapper = useRef(null);
    const { screenToFlowPosition } = useReactFlow();

    const nodes = useStore((state) => state.nodes);
    const edges = useStore((state) => state.edges);
    const onNodesChange = useStore((state) => state.onNodesChange);
    const onEdgesChange = useStore((state) => state.onEdgesChange);
    const onConnect = useStore((state) => state.onConnect);
    const addNode = useStore((state) => state.addNode);
    const setSelectedId = useStore((state) => state.setSelectedId);
    const deleteNodes = useStore((state) => state.deleteNodes);
    const selectedId = useStore((state) => state.selectedId);

    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [nodesToDelete, setNodesToDelete] = useState([]);

    // Fetch initial data - DISABLED: Start with empty canvas
    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             const response = await axios.get(`/policies/${policyId}/graph`);
    //             const { nodes: apiNodes, edges: apiEdges } = response.data;

    //             const validNodes = apiNodes.map(node => ({
    //                 ...node,
    //                 type: node.type || 'host',
    //                 position: node.position || { x: 0, y: 0 }
    //             }));

    //             useStore.setState({ nodes: validNodes, edges: apiEdges });
    //         } catch (error) {
    //             console.error("Error fetching graph data:", error);
    //             // Start with empty canvas if API fails
    //         }
    //     };

    //     fetchData();
    // }, [policyId]);

    const onDragOver = useCallback((event) => {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    }, []);

    const onDrop = useCallback(
        (event) => {
            event.preventDefault();

            const type = event.dataTransfer.getData('application/reactflow');

            // check if the dropped element is valid
            if (typeof type === 'undefined' || !type) {
                return;
            }

            const position = screenToFlowPosition({
                x: event.clientX,
                y: event.clientY,
            });

            const newNode = {
                id: `${type}-${Date.now()}`,
                type,
                position,
                data: { label: `New ${type}` },
            };

            addNode(newNode);
        },
        [screenToFlowPosition, addNode],
    );

    const onSelectionChange = useCallback(({ nodes, edges }) => {
        if (nodes.length > 0) {
            setSelectedId(nodes[0].id);
        } else if (edges.length > 0) {
            setSelectedId(edges[0].id);
        } else {
            setSelectedId(null);
        }
    }, [setSelectedId]);

    const handleDeleteClick = useCallback(() => {
        const selectedNodes = nodes.filter(n => n.selected);
        if (selectedNodes.length > 0) {
            setNodesToDelete(selectedNodes.map(n => n.id));
            setDeleteDialogOpen(true);
        }
    }, [nodes]);

    const handleConfirmDelete = useCallback(() => {
        deleteNodes(nodesToDelete);
        setDeleteDialogOpen(false);
        setNodesToDelete([]);
    }, [deleteNodes, nodesToDelete]);

    const handleCancelDelete = useCallback(() => {
        setDeleteDialogOpen(false);
        setNodesToDelete([]);
    }, []);

    // Keyboard handler for Delete key
    useEffect(() => {
        const handleKeyDown = (event) => {
            if ((event.key === 'Delete' || event.key === 'Backspace') && selectedId) {
                const selectedNode = nodes.find(n => n.id === selectedId);
                if (selectedNode) {
                    handleDeleteClick();
                }
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [selectedId, nodes, handleDeleteClick]);

    return (
        <div className="flex h-screen w-screen overflow-hidden" style={{ height: '100vh', width: '100vw' }}>
            <Sidebar />
            <div className="flex-grow h-full" ref={reactFlowWrapper} style={{ height: '100%', width: '100%' }}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onDragOver={onDragOver}
                    onDrop={onDrop}
                    onSelectionChange={onSelectionChange}
                    nodeTypes={nodeTypes}
                    fitView
                    className="bg-gray-50"
                >
                    <Controls />
                    <MiniMap />
                    <Background variant="dots" gap={12} size={1} />
                    <Panel position="top-right" className="bg-white p-2 rounded shadow-sm text-xs text-gray-500">
                        React Flow Firewall Visualizer
                    </Panel>
                </ReactFlow>
            </div>
            <PropertiesPanel />
            <DeleteConfirmDialog
                isOpen={deleteDialogOpen}
                onConfirm={handleConfirmDelete}
                onCancel={handleCancelDelete}
                itemType="Node"
                itemCount={nodesToDelete.length}
            />
        </div>
    );
}

export default function Flow(props) {
    return (
        <ReactFlowProvider>
            <FlowContent {...props} />
        </ReactFlowProvider>
    );
}
