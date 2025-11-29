import { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ChevronRight, Edit, Trash2 } from 'lucide-react';
import { useServiceById } from '../hooks/useServices';
import ServiceBadge from '../components/common/ServiceBadge';
import StatusIndicator from '../components/common/StatusIndicator';
import OverviewTab from '../components/services/tabs/OverviewTab';
import HostsTab from '../components/services/tabs/HostsTab';
import NetworksTab from '../components/services/tabs/NetworksTab';
import GroupsTab from '../components/services/tabs/GroupsTab';
import PoliciesTab from '../components/services/tabs/PoliciesTab';

const TABS = ['overview', 'hosts', 'networks', 'groups', 'policies'];

export default function ServiceDetailView({ tab: initialTab }) {
  const { serviceId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(initialTab || 'overview');
  const { data: service, isLoading } = useServiceById(parseInt(serviceId));

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-slate-400">Loading service...</div>
      </div>
    );
  }

  if (!service) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4">
        <div className="text-slate-400">Service not found</div>
        <Link to="/services" className="text-indigo-400 hover:text-indigo-300">
          Back to Services
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 text-sm text-slate-400">
        <Link to="/services" className="hover:text-indigo-400 transition-colors">
          Services
        </Link>
        <ChevronRight className="w-4 h-4" />
        <span className="text-slate-200">{service.shortName}</span>
      </div>

      <div className="flex items-start justify-between">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-gradient-to-br from-blue-600/20 to-indigo-600/20 rounded-2xl">
            <StatusIndicator status={service.status} size="lg" />
          </div>
          <div>
            <div className="flex items-center gap-3 mb-2">
              <ServiceBadge shortName={service.shortName} status={service.status} />
              <h1 className="text-2xl font-bold text-slate-50">{service.fullName}</h1>
            </div>
            <p className="text-sm text-slate-400">{service.description}</p>
            <div className="flex items-center gap-4 mt-2 text-xs text-slate-500">
              <span>Category: <span className="text-slate-300">{service.category}</span></span>
              <span>Firewall: <span className="text-slate-300">{service.firewall}</span></span>
              <span>Owner: <span className="text-slate-300">{service.owner}</span></span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 text-slate-200 border border-white/10 rounded-lg transition-all">
            <Edit className="w-4 h-4" />
            Edit
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-lg transition-all">
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-5">
          <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">Hosts</p>
          <p className="text-3xl font-bold text-slate-50">{service.hostsCount}</p>
        </div>
        <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-5">
          <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">Networks</p>
          <p className="text-3xl font-bold text-slate-50">{service.networksCount}</p>
        </div>
        <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-5">
          <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">Groups</p>
          <p className="text-3xl font-bold text-slate-50">{service.groupsCount}</p>
        </div>
        <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-5">
          <p className="text-xs uppercase tracking-wide text-slate-500 mb-1">Policies</p>
          <p className="text-3xl font-bold text-slate-50">{service.policiesCount}</p>
        </div>
      </div>

      <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl overflow-hidden">
        <div className="border-b border-white/10 px-6 pt-4">
          <nav className="flex gap-1">
            {TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => {
                  setActiveTab(tab);
                  navigate(`/services/${serviceId}${tab === 'overview' ? '' : `/${tab}`}`);
                }}
                className={`px-4 py-3 text-sm font-medium rounded-t-lg transition-all capitalize ${
                  activeTab === tab
                    ? 'border-b-2 border-indigo-500 text-indigo-400 bg-white/5'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && <OverviewTab service={service} />}
          {activeTab === 'hosts' && <HostsTab serviceId={service.id} />}
          {activeTab === 'networks' && <NetworksTab serviceId={service.id} />}
          {activeTab === 'groups' && <GroupsTab serviceId={service.id} />}
          {activeTab === 'policies' && <PoliciesTab serviceId={service.id} />}
        </div>
      </div>
    </div>
  );
}
