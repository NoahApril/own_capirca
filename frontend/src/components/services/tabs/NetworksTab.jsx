import { Plus } from 'lucide-react';
import { useServiceNetworks } from '../../../hooks/useServices';

export default function NetworksTab({ serviceId }) {
  const { data: networks, isLoading } = useServiceNetworks(serviceId);

  if (isLoading) {
    return <div className="text-slate-400">Loading networks...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{networks?.length || 0} networks in this service</p>
        <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 rounded-lg text-sm font-medium transition-all">
          <Plus className="w-4 h-4" />
          Add Network
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-900/50 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <tr>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">CIDR</th>
              <th className="px-4 py-3 text-left">Comment</th>
              <th className="px-4 py-3 text-center">Used in Policies</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {networks?.map((network) => (
              <tr key={network.id} className="hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 text-sm font-medium text-slate-200">{network.name}</td>
                <td className="px-4 py-3 text-sm text-slate-300">{network.ipAddress}</td>
                <td className="px-4 py-3 text-sm text-slate-400">{network.comment}</td>
                <td className="px-4 py-3 text-center text-sm text-slate-300">{network.usedInPoliciesCount}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
