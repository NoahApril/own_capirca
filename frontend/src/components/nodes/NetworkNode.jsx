import { Handle, Position } from '@xyflow/react';
import { Cloud, ChevronDown, ChevronRight } from 'lucide-react';
import { useState, useMemo } from 'react';

const NetworkNode = ({ data, selected }) => {
    const [expanded, setExpanded] = useState(false);

    // Calculate network information from CIDR
    const networkInfo = useMemo(() => {
        if (!data.cidr) return null;

        const [ip, bits] = data.cidr.split('/');
        const bitsNum = parseInt(bits);
        const maxHosts = Math.pow(2, 32 - bitsNum) - 2; // -2 for network and broadcast

        return {
            ip,
            bits: bitsNum,
            maxHosts: maxHosts > 0 ? maxHosts : 1,
            netmask: calculateNetmask(bitsNum)
        };
    }, [data.cidr]);

    function calculateNetmask(bits) {
        const mask = [];
        for (let i = 0; i < 4; i++) {
            const n = Math.min(bits, 8);
            mask.push(256 - Math.pow(2, 8 - n));
            bits -= n;
        }
        return mask.join('.');
    }

    return (
        <div
            className={`shadow-md rounded-lg bg-white border-4 border-double min-w-[150px] transition-all ${selected ? 'border-green-500' : 'border-green-300'
                }`}
        >
            <div className="flex items-center justify-between px-4 py-2.5">
                <div className="flex items-center">
                    <div className="rounded-full w-8 h-8 flex items-center justify-center bg-green-100 text-green-600">
                        <Cloud size={16} />
                    </div>
                    <div className="ml-2">
                        <div className="text-sm font-bold text-gray-700">{data.label}</div>
                        <div className="text-xs text-gray-500">{data.cidr || '0.0.0.0/0'}</div>
                    </div>
                </div>
                {networkInfo && (
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

            {expanded && networkInfo && (
                <div className="px-3 py-2 bg-gray-50 border-t border-gray-100">
                    <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
                        Network Details
                    </div>
                    <div className="space-y-1 text-xs">
                        <div className="flex justify-between bg-white rounded px-2 py-1 border border-gray-200">
                            <span className="text-gray-500">Network:</span>
                            <span className="font-medium text-gray-700">{networkInfo.ip}</span>
                        </div>
                        <div className="flex justify-between bg-white rounded px-2 py-1 border border-gray-200">
                            <span className="text-gray-500">Netmask:</span>
                            <span className="font-medium text-gray-700">{networkInfo.netmask}</span>
                        </div>
                        <div className="flex justify-between bg-white rounded px-2 py-1 border border-gray-200">
                            <span className="text-gray-500">CIDR Bits:</span>
                            <span className="font-medium text-gray-700">/{networkInfo.bits}</span>
                        </div>
                        <div className="flex justify-between bg-white rounded px-2 py-1 border border-gray-200">
                            <span className="text-gray-500">Max Hosts:</span>
                            <span className="font-medium text-gray-700">{networkInfo.maxHosts.toLocaleString()}</span>
                        </div>
                    </div>
                </div>
            )}

            <Handle
                type="target"
                position={Position.Left}
                className="w-3 h-3 !bg-green-400"
            />
            <Handle
                type="source"
                position={Position.Right}
                className="w-3 h-3 !bg-green-400"
            />
        </div>
    );
};

export default NetworkNode;
