import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Search, LayoutGrid, List as ListIcon } from 'lucide-react';
import { useServices } from '../hooks/useServices';
import ServiceCard from '../components/services/ServiceCard';
import StatusIndicator from '../components/common/StatusIndicator';

export default function ServicesOverview() {
  const { data: services, isLoading } = useServices();
  const [viewMode, setViewMode] = useState('grid');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredServices = services?.filter((service) =>
    service.shortName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.fullName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-slate-400">Loading services...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-50 mb-1">Services ({services?.length || 0})</h1>
          <p className="text-sm text-slate-400">Manage your IT services and firewall configurations</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-indigo-500/30 rounded-lg font-medium transition-all">
          <Plus className="w-4 h-4" />
          New Service
        </button>
      </div>

      <div className="flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search services..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-950/50 border border-white/10 rounded-lg text-slate-200 placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          />
        </div>

        <div className="flex items-center gap-2 bg-slate-800/40 border border-white/5 rounded-lg p-1">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
            aria-label="Grid view"
          >
            <LayoutGrid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-2 rounded-lg transition-all ${viewMode === 'list' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
            aria-label="List view"
          >
            <ListIcon className="w-4 h-4" />
          </button>
        </div>
      </div>

      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredServices?.map((service) => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      ) : (
        <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-900/50 text-xs font-semibold text-slate-400 uppercase tracking-wider border-b border-white/5">
              <tr>
                <th className="px-6 py-4 text-left">Service</th>
                <th className="px-6 py-4 text-left">Status</th>
                <th className="px-6 py-4 text-center">Hosts</th>
                <th className="px-6 py-4 text-center">Networks</th>
                <th className="px-6 py-4 text-center">Groups</th>
                <th className="px-6 py-4 text-center">Policies</th>
                <th className="px-6 py-4 text-center">Expiring</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {filteredServices?.map((service) => (
                <tr key={service.id} className="hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4">
                    <Link to={`/services/${service.id}`} className="flex items-center gap-3">
                      <div>
                        <p className="font-semibold text-slate-200">{service.shortName}</p>
                        <p className="text-xs text-slate-500">{service.fullName}</p>
                      </div>
                    </Link>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <StatusIndicator status={service.status} size="sm" />
                      <span className="text-sm text-slate-300 capitalize">{service.status}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-center text-sm text-slate-300">{service.hostsCount}</td>
                  <td className="px-6 py-4 text-center text-sm text-slate-300">{service.networksCount}</td>
                  <td className="px-6 py-4 text-center text-sm text-slate-300">{service.groupsCount}</td>
                  <td className="px-6 py-4 text-center text-sm text-slate-300">{service.policiesCount}</td>
                  <td className="px-6 py-4 text-center">
                    {service.policiesExpiringCount > 0 ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
                        {service.policiesExpiringCount}
                      </span>
                    ) : (
                      <span className="text-sm text-slate-500">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
