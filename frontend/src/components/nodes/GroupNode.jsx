import { Handle, Position } from '@xyflow/react';
import { Layers, ChevronDown, ChevronRight, Server, Cloud } from 'lucide-react';
import { useState, useMemo } from 'react';
import { mockHosts, mockNetworks } from '../../utils/mockData';

const GroupNode = ({ data, selected }) => {
    const [expanded, setExpanded] = useState(false);

    // Resolve member IDs to actual objects
    const members = useMemo(() => {
        if (!data.members || !Array.isArray(data.members)) return [];

        return data.members.map(memberId => {
            // Try to find in hosts first
            let member = mockHosts.find(h => h.id === memberId);
            if (member) return { ...member, type: 'host' };

            // Try to find in networks
            member = mockNetworks.find(n => n.id === memberId);
            if (member) return { ...member, type: 'network' };

            return null;
        }).filter(Boolean);
    }, [data.members]);

    return (
        <div
            className={`shadow-md rounded-lg bg-white border-4 border-dashed min-w-[200px] transition-all ${selected ? 'border-purple-500' : 'border-purple-300'
                }`}
        >
            <div className="px-4 py-2.5 flex items-center justify-between">
                <div className="flex items-center">
                    <div className="rounded-full w-8 h-8 flex items-center justify-center bg-purple-100 text-purple-600">
                        <Layers size={16} />
                    </div>
                    <div className="ml-2">
                        <div className="text-sm font-bold text-gray-700">{data.label}</div>
                        <div className="text-xs text-gray-500">
                            {members.length} {members.length === 1 ? 'Member' : 'Members'}
                        </div>
                    </div>
                </div>
                {members.length > 0 && (
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            setExpanded(!expanded);
                        }}
                        className="p-1 hover:bg-gray-100 rounded text-gray-500"
                    >
                        {expanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                    </button>
                )}
            </div>

            {expanded && members.length > 0 && (
                <div className="px-3 py-2 bg-gray-50 border-t border-gray-100 max-h-64 overflow-y-auto">
                    <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
                        Members ({members.length})
                    </div>
                    <div className="space-y-1">
                        {members.map((member, index) => (
                            <div
                                key={index}
                                className="flex items-start text-xs bg-white rounded px-2 py-1.5 border border-gray-200"
                            >
                                {member.type === 'host' ? (
                                    <Server size={12} className="text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                                ) : (
                                    <Cloud size={12} className="text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                                )}
                                <div className="flex-1 min-w-0">
                                    <div className="font-medium text-gray-700 truncate" title={member.name}>
                                        {member.name}
                                    </div>
                                    <div className="text-gray-500 text-[10px]">
                                        {member.type === 'host'
                                            ? (member.fqdn || 'Host')
                                            : (member.cidr || 'Network')}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <Handle
                type="target"
                position={Position.Left}
                style={{ top: '50%' }}
                className="w-3 h-3 !bg-purple-400"
            />
            <Handle
                type="source"
                position={Position.Right}
                style={{ top: '50%' }}
                className="w-3 h-3 !bg-purple-400"
            />
        </div>
    );
};

export default GroupNode;
