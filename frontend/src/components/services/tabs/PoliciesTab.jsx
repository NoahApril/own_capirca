import { Plus } from 'lucide-react';
import { useServicePolicies } from '../../../hooks/useServices';

export default function PoliciesTab({ serviceId }) {
  const { data: policies, isLoading } = useServicePolicies(serviceId);

  if (isLoading) {
    return <div className="text-slate-400">Loading policies...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{policies?.length || 0} policies in this service</p>
        <button className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-indigo-500/30 rounded-lg text-sm font-medium transition-all">
          <Plus className="w-4 h-4" />
          Create Policy
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-900/50 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <tr>
              <th className="px-4 py-3 text-left">Source</th>
              <th className="px-4 py-3 text-left">Destination</th>
              <th className="px-4 py-3 text-left">Services</th>
              <th className="px-4 py-3 text-left">Action</th>
              <th className="px-4 py-3 text-left">Expires</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {policies?.map((policy) => (
              <tr key={policy.id} className="hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 text-sm text-slate-300">{policy.source.join(', ')}</td>
                <td className="px-4 py-3 text-sm text-slate-300">{policy.destination.join(', ')}</td>
                <td className="px-4 py-3 text-sm text-slate-300">
                  {policy.services.map((svc) => `${svc.name} (${svc.protocol}${svc.port ? `:${svc.port}` : ''})`).join(', ')}
                </td>
                <td className="px-4 py-3 text-sm font-semibold capitalize text-slate-200">{policy.action}</td>
                <td className="px-4 py-3 text-sm text-slate-400">
                  {policy.expiresAt ? new Date(policy.expiresAt).toLocaleString() : 'N/A'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
