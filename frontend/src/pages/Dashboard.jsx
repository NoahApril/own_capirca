import { Building2, Server, Network, Users, Shield } from 'lucide-react';
import StatsCard from '../components/dashboard/StatsCard';
import ServiceHealthOverview from '../components/dashboard/ServiceHealthOverview';
import RecentActivity from '../components/dashboard/RecentActivity';
import ExpiringPoliciesAlert from '../components/dashboard/ExpiringPoliciesAlert';
import TopServicesChart from '../components/dashboard/TopServicesChart';
import { useDashboardStats, useRecentActivity, useExpiringPolicies } from '../hooks/useDashboardData';

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useDashboardStats();
  const { data: activities, isLoading: activitiesLoading } = useRecentActivity();
  const { data: expiringPolicies, isLoading: expiringLoading } = useExpiringPolicies();

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-slate-400">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-50 mb-1">Dashboard</h1>
        <p className="text-sm text-slate-400">Service-Oriented Firewall Management Overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatsCard title="Services" value={stats.servicesCount} icon={Building2} />
        <StatsCard title="Hosts" value={stats.hostsCount} change={stats.hostsChange} icon={Server} />
        <StatsCard title="Networks" value={stats.networksCount} change={stats.networksChange} icon={Network} />
        <StatsCard title="Groups" value={stats.groupsCount} change={stats.groupsChange} icon={Users} />
        <StatsCard title="Policies" value={stats.policiesCount} change={stats.policiesChange} icon={Shield} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ServiceHealthOverview stats={stats} />
        <TopServicesChart services={stats.topServices} />
      </div>

      {!expiringLoading && expiringPolicies && expiringPolicies.length > 0 && (
        <ExpiringPoliciesAlert policies={expiringPolicies} />
      )}

      {!activitiesLoading && activities && (
        <RecentActivity activities={activities} />
      )}
    </div>
  );
}
