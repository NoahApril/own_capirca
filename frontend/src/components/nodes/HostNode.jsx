import { Handle, Position } from '@xyflow/react';
import { Server } from 'lucide-react';

const HostNode = ({ data, selected }) => {
    return (
        <div
            className="px-4 py-2.5 shadow-md rounded-lg bg-white min-w-[150px] transition-all"
            style={{
                borderWidth: '2px',
                borderStyle: 'solid',
                borderColor: selected ? '#3b82f6' : '#bfdbfe',
                boxSizing: 'border-box'
            }}
        >
            <div className="flex items-center">
                <div className="rounded-full w-8 h-8 flex items-center justify-center bg-blue-100 text-blue-600">
                    <Server size={16} />
                </div>
                <div className="ml-2 flex-1 min-w-0">
                    <div className="text-sm font-bold text-gray-700 truncate" title={data.label}>
                        {data.label}
                    </div>
                    <div className="text-xs text-gray-500 truncate" title={data.fqdn || data.ip}>
                        {data.fqdn || data.ip || 'Host'}
                    </div>
                </div>
            </div>

            <Handle
                type="target"
                position={Position.Left}
                style={{ top: '50%' }}
                className="w-3 h-3 !bg-blue-400"
            />
            <Handle
                type="source"
                position={Position.Right}
                style={{ top: '50%' }}
                className="w-3 h-3 !bg-blue-400"
            />
        </div>
    );
};

export default HostNode;
