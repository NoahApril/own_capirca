import { Plus } from 'lucide-react';
import { useServiceHosts } from '../../../hooks/useServices';

export default function HostsTab({ serviceId }) {
  const { data: hosts, isLoading } = useServiceHosts(serviceId);

  if (isLoading) {
    return <div className="text-slate-400">Loading hosts...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{hosts?.length || 0} hosts in this service</p>
        <button className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-indigo-500/30 rounded-lg text-sm font-medium transition-all">
          <Plus className="w-4 h-4" />
          Add Host
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-900/50 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <tr>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">IP Address</th>
              <th className="px-4 py-3 text-left">Type</th>
              <th className="px-4 py-3 text-left">Comment</th>
              <th className="px-4 py-3 text-center">Used in Policies</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {hosts?.map((host) => (
              <tr key={host.id} className="hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 text-sm font-medium text-slate-200">{host.name}</td>
                <td className="px-4 py-3 text-sm text-slate-300">{host.ipAddress}</td>
                <td className="px-4 py-3 text-sm text-slate-400">{host.type}</td>
                <td className="px-4 py-3 text-sm text-slate-400">{host.comment}</td>
                <td className="px-4 py-3 text-center text-sm text-slate-300">{host.usedInPoliciesCount}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
