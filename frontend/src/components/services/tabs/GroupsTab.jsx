import { Plus } from 'lucide-react';
import { useServiceGroups } from '../../../hooks/useServices';

export default function GroupsTab({ serviceId }) {
  const { data: groups, isLoading } = useServiceGroups(serviceId);

  if (isLoading) {
    return <div className="text-slate-400">Loading groups...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{groups?.length || 0} groups in this service</p>
        <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 rounded-lg text-sm font-medium transition-all">
          <Plus className="w-4 h-4" />
          Add Group
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-900/50 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <tr>
              <th className="px-4 py-3 text-left">Name</th>
              <th className="px-4 py-3 text-left">Type</th>
              <th className="px-4 py-3 text-center">Members</th>
              <th className="px-4 py-3 text-left">Comment</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {groups?.map((group) => (
              <tr key={group.id} className="hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 text-sm font-medium text-slate-200">{group.name}</td>
                <td className="px-4 py-3 text-sm text-slate-400 capitalize">{group.type}</td>
                <td className="px-4 py-3 text-center text-sm text-slate-300">{group.members.length}</td>
                <td className="px-4 py-3 text-sm text-slate-400">{group.comment}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
