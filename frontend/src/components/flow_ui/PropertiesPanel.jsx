import useStore from '../../store/useFlowStore';
import { mockHosts, mockNetworks, mockGroups } from '../../utils/mockData';

const PropertiesPanel = () => {
    const { selectedId, nodes, edges, updateNode, updateEdge } = useStore();

    const selectedNode = nodes.find((n) => n.id === selectedId);
    const selectedEdge = edges.find((e) => e.id === selectedId);

    if (!selectedId) {
        return (
            <aside className="w-80 bg-white border-l border-gray-200 p-6 flex flex-col items-center justify-center text-center h-full">
                <div className="text-gray-400 mb-2">Select an item</div>
                <div className="text-sm text-gray-500">
                    Click on a node or edge to view and edit its properties.
                </div>
            </aside>
        );
    }

    const handleObjectSelect = (e) => {
        const objectId = e.target.value;
        if (!objectId) return;

        let selectedObject;
        if (selectedNode.type === 'host') {
            selectedObject = mockHosts.find(h => h.id === objectId);
            if (selectedObject) {
                updateNode(selectedId, {
                    label: selectedObject.name,
                    fqdn: selectedObject.fqdn
                });
            }
        } else if (selectedNode.type === 'network') {
            selectedObject = mockNetworks.find(n => n.id === objectId);
            if (selectedObject) {
                updateNode(selectedId, {
                    label: selectedObject.name,
                    cidr: selectedObject.cidr,
                    description: selectedObject.description
                });
            }
        } else if (selectedNode.type === 'net_group') {
            selectedObject = mockGroups.find(g => g.id === objectId);
            if (selectedObject) {
                updateNode(selectedId, {
                    label: selectedObject.name,
                    members: selectedObject.members,
                    count: selectedObject.members.length
                });
            }
        }
    };

    return (
        <aside className="w-80 bg-white border-l border-gray-200 flex flex-col h-full overflow-y-auto">
            <div className="p-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-800">Properties</h2>
                <p className="text-xs text-gray-500">ID: {selectedId}</p>
            </div>

            <div className="p-4 space-y-4">
                {selectedNode && (
                    <>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Select Object</label>
                            <select
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                onChange={handleObjectSelect}
                                defaultValue=""
                            >
                                <option value="" disabled>Select {selectedNode.type}...</option>
                                {selectedNode.type === 'host' && mockHosts.map(h => (
                                    <option key={h.id} value={h.id}>{h.name}</option>
                                ))}
                                {selectedNode.type === 'network' && mockNetworks.map(n => (
                                    <option key={n.id} value={n.id}>{n.name} ({n.cidr})</option>
                                ))}
                                {selectedNode.type === 'net_group' && mockGroups.map(g => (
                                    <option key={g.id} value={g.id}>{g.name}</option>
                                ))}
                            </select>
                        </div>

                        <div className="pt-4 border-t border-gray-100">
                            <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Current Values</div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Label</label>
                                <input
                                    type="text"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                                    value={selectedNode.data.label}
                                    readOnly
                                />
                            </div>

                            {selectedNode.type === 'host' && (
                                <div className="mt-2">
                                    <label className="block text-sm font-medium text-gray-700 mb-1">FQDN</label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                                        value={selectedNode.data.fqdn || selectedNode.data.ip || ''}
                                        readOnly
                                    />
                                </div>
                            )}

                            {selectedNode.type === 'network' && (
                                <div className="mt-2">
                                    <label className="block text-sm font-medium text-gray-700 mb-1">CIDR</label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                                        value={selectedNode.data.cidr || ''}
                                        readOnly
                                    />
                                </div>
                            )}

                            {(selectedNode.type === 'net_group') && (
                                <div className="mt-2">
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Members</label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                                        value={selectedNode.data.count || 0}
                                        readOnly
                                    />
                                </div>
                            )}
                        </div>
                    </>
                )}

                {selectedEdge && (
                    <>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Action</label>
                            <select
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                value={selectedEdge.data?.action || 'allow'}
                                onChange={(e) => updateEdge(selectedId, { action: e.target.value })}
                            >
                                <option value="allow">Allow</option>
                                <option value="deny">Deny</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Protocol</label>
                            <select
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                value={selectedEdge.data?.protocol || 'tcp'}
                                onChange={(e) => updateEdge(selectedId, { protocol: e.target.value })}
                            >
                                <option value="tcp">TCP</option>
                                <option value="udp">UDP</option>
                                <option value="icmp">ICMP</option>
                                <option value="any">Any</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Ports</label>
                            <input
                                type="text"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                value={selectedEdge.data?.ports || ''}
                                onChange={(e) => updateEdge(selectedId, { ports: e.target.value })}
                                placeholder="e.g. 80, 443"
                            />
                        </div>
                    </>
                )}
            </div>
        </aside>
    );
};

export default PropertiesPanel;
