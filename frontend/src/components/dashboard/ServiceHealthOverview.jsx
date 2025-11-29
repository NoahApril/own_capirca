import { useServiceHealth } from '../../hooks/useDashboardData';
import StatusIndicator from '../common/StatusIndicator';

export default function ServiceHealthOverview({ stats }) {
  const { data: healthData, isLoading } = useServiceHealth();

  return (
    <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-semibold text-slate-50">Service Health Overview</h2>
          <p className="text-sm text-slate-400">Overall service status distribution</p>
        </div>
        <div className="flex items-center gap-6 text-sm text-slate-300">
          <div className="flex items-center gap-2">
            <StatusIndicator status="healthy" size="sm" />
            <span>{stats.servicesHealthy} Healthy</span>
          </div>
          <div className="flex items-center gap-2">
            <StatusIndicator status="warning" size="sm" />
            <span>{stats.servicesWarning} Warning</span>
          </div>
          <div className="flex items-center gap-2">
            <StatusIndicator status="critical" size="sm" />
            <span>{stats.servicesCritical} Critical</span>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {isLoading && <div className="text-sm text-slate-500">Loading service health...</div>}
        {!isLoading && healthData && healthData.map((service) => (
          <div key={service.id} className="flex items-center justify-between bg-white/5 rounded-lg px-4 py-3">
            <div className="flex items-center gap-3">
              <StatusIndicator status={service.status} />
              <div>
                <p className="font-medium text-slate-200">{service.name}</p>
                <p className="text-xs text-slate-500">{service.policiesCount} policies</p>
              </div>
            </div>
            {service.expiringPolicies > 0 ? (
              <span className="text-xs font-semibold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-3 py-1 rounded-full">
                {service.expiringPolicies} expiring
              </span>
            ) : (
              <span className="text-xs text-slate-400">Stable</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
