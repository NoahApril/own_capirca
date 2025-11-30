import { ArrowRight, AlertTriangle } from 'lucide-react';
import { Link } from 'react-router-dom';
import ServiceBadge from '../common/ServiceBadge';
import StatusIndicator from '../common/StatusIndicator';

export default function ServiceCard({ service }) {
  const statusGradients = {
    healthy: 'from-emerald-500/10 via-emerald-500/5 to-transparent border-emerald-500/5',
    warning: 'from-amber-500/10 via-amber-500/5 to-transparent border-amber-500/5',
    critical: 'from-rose-500/10 via-rose-500/5 to-transparent border-rose-500/5',
  };

  return (
    <Link
      to={`/services/${service.id}`}
      className={`bg-gradient-to-br ${statusGradients[service.status]} backdrop-blur-md border rounded-2xl shadow-xl p-5 hover:border-white/15 transition-all block group`}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <ServiceBadge shortName={service.shortName} status={service.status} />
          <h3 className="text-lg font-semibold text-slate-50 mt-3">{service.fullName}</h3>
          <p className="text-sm text-slate-400 mt-1">{service.category}</p>
        </div>
        <div className="p-2 bg-white/5 rounded-xl">
          <StatusIndicator status={service.status} size="lg" />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm text-slate-300">
        <div className="bg-white/5 rounded-xl px-3 py-2">
          <p className="text-xs uppercase tracking-wide text-slate-500">Hosts</p>
          <p className="text-lg font-semibold text-slate-50">{service.hostsCount}</p>
        </div>
        <div className="bg-white/5 rounded-xl px-3 py-2">
          <p className="text-xs uppercase tracking-wide text-slate-500">Networks</p>
          <p className="text-lg font-semibold text-slate-50">{service.networksCount}</p>
        </div>
        <div className="bg-white/5 rounded-xl px-3 py-2">
          <p className="text-xs uppercase tracking-wide text-slate-500">Groups</p>
          <p className="text-lg font-semibold text-slate-50">{service.groupsCount}</p>
        </div>
        <div className="bg-white/5 rounded-xl px-3 py-2">
          <p className="text-xs uppercase tracking-wide text-slate-500">Policies</p>
          <p className="text-lg font-semibold text-slate-50">{service.policiesCount}</p>
        </div>
      </div>

      <div className="flex items-center justify-between mt-5 text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <span className="font-medium text-slate-300">Firewall</span>
          <span>{service.firewall}</span>
        </div>
        {service.policiesExpiringCount > 0 && (
          <span className="inline-flex items-center gap-1 text-amber-400 font-semibold">
            <AlertTriangle className="w-3 h-3" />
            {service.policiesExpiringCount} expiring
          </span>
        )}
      </div>

      <div className="flex items-center gap-2 text-indigo-400 text-sm font-medium mt-4">
        View Details
        <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
      </div>
    </Link>
  );
}
