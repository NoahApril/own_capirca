import { Monitor, Cloud, Layers } from 'lucide-react';

const Sidebar = () => {
    const onDragStart = (event, nodeType) => {
        event.dataTransfer.setData('application/reactflow', nodeType);
        event.dataTransfer.effectAllowed = 'move';
    };

    return (
        <aside className="w-64 bg-white border-r border-gray-200 flex flex-col h-full">
            <div className="p-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-800">Components</h2>
                <p className="text-xs text-gray-500">Drag to add to canvas</p>
            </div>

            <div className="p-4 space-y-3">
                <div
                    className="flex items-center p-3 bg-white border border-gray-200 rounded-md cursor-grab hover:border-blue-500 hover:shadow-sm transition-all"
                    onDragStart={(event) => onDragStart(event, 'host')}
                    draggable
                >
                    <div className="p-2 bg-blue-100 rounded-md text-blue-600 mr-3">
                        <Monitor size={20} />
                    </div>
                    <div>
                        <div className="text-sm font-medium text-gray-700">Host</div>
                        <div className="text-xs text-gray-500">Single IP/Entity</div>
                    </div>
                </div>

                <div
                    className="flex items-center p-3 bg-white border border-gray-200 rounded-md cursor-grab hover:border-green-500 hover:shadow-sm transition-all"
                    onDragStart={(event) => onDragStart(event, 'network')}
                    draggable
                >
                    <div className="p-2 bg-green-100 rounded-md text-green-600 mr-3">
                        <Cloud size={20} />
                    </div>
                    <div>
                        <div className="text-sm font-medium text-gray-700">Network</div>
                        <div className="text-xs text-gray-500">Subnet/CIDR</div>
                    </div>
                </div>

                <div
                    className="flex items-center p-3 bg-white border border-gray-200 rounded-md cursor-grab hover:border-purple-500 hover:shadow-sm transition-all"
                    onDragStart={(event) => onDragStart(event, 'net_group')}
                    draggable
                >
                    <div className="p-2 bg-purple-100 rounded-md text-purple-600 mr-3">
                        <Layers size={20} />
                    </div>
                    <div>
                        <div className="text-sm font-medium text-gray-700">Group</div>
                        <div className="text-xs text-gray-500">Collection</div>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
