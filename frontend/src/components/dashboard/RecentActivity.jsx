import { Activity, Plus, Trash2, Edit } from 'lucide-react';
import ServiceBadge from '../common/ServiceBadge';

export default function RecentActivity({ activities }) {
  const getActionIcon = (action) => {
    switch (action) {
      case 'created':
        return <Plus className="w-4 h-4 text-emerald-400" />;
      case 'updated':
        return <Edit className="w-4 h-4 text-blue-400" />;
      case 'deleted':
        return <Trash2 className="w-4 h-4 text-rose-400" />;
      default:
        return <Activity className="w-4 h-4 text-slate-400" />;
    }
  };

  const getActionColor = (action) => {
    switch (action) {
      case 'created':
        return 'text-emerald-300';
      case 'updated':
        return 'text-blue-300';
      case 'deleted':
        return 'text-rose-300';
      default:
        return 'text-slate-300';
    }
  };

  return (
    <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-6">
      <div className="flex items-center gap-3 mb-6">
        <Activity className="w-5 h-5 text-indigo-400" />
        <div>
          <h2 className="text-lg font-semibold text-slate-50">Recent Activity</h2>
          <p className="text-sm text-slate-400">Latest changes across all services</p>
        </div>
      </div>

      <div className="space-y-3">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-center gap-4 bg-white/5 rounded-lg px-4 py-3 hover:bg-white/10 transition-all">
            <div className="flex-shrink-0">
              {getActionIcon(activity.action)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className={`text-sm font-semibold capitalize ${getActionColor(activity.action)}`}>
                  {activity.action}
                </span>
                <span className="text-sm text-slate-400">{activity.type}</span>
                <span className="text-sm text-slate-500">in</span>
                <ServiceBadge shortName={activity.serviceName} status="healthy" />
              </div>
              <p className="text-sm text-slate-300 truncate">{activity.entityName}</p>
            </div>
            <div className="flex-shrink-0 text-xs text-slate-500">
              {new Date(activity.timestamp).toLocaleString('de-DE', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
