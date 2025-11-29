import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Building2, 
  Server, 
  Network, 
  Users, 
  Shield,
  ChevronRight
} from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

const navigation = [
  { name: 'Dashboard', to: '/', icon: LayoutDashboard },
  { name: 'Services', to: '/services', icon: Building2 },
];

const globalNavigation = [
  { name: 'All Hosts', to: '/global/hosts', icon: Server },
  { name: 'All Networks', to: '/global/networks', icon: Network },
  { name: 'All Groups', to: '/global/groups', icon: Users },
  { name: 'All Policies', to: '/global/policies', icon: Shield },
];

export default function Sidebar() {
  const location = useLocation();
  const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);

  const isActive = (path) => location.pathname === path;

  return (
    <aside 
      className={`
        flex flex-col bg-slate-950 border-r border-white/5 transition-all duration-300
        ${sidebarCollapsed ? 'w-20' : 'w-64'}
      `}
    >
      <div className="flex items-center justify-between h-16 px-4 border-b border-white/5">
        {!sidebarCollapsed && (
          <div className="flex items-center gap-2">
            <Shield className="w-6 h-6 text-indigo-400" />
            <span className="text-lg font-bold text-slate-50">Firewall</span>
          </div>
        )}
        {sidebarCollapsed && (
          <Shield className="w-6 h-6 text-indigo-400 mx-auto" />
        )}
      </div>

      <nav className="flex-1 overflow-y-auto py-4">
        <div className="px-3 mb-6">
          {!sidebarCollapsed && (
            <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Main
            </p>
          )}
          <div className="space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.to);
              
              return (
                <Link
                  key={item.name}
                  to={item.to}
                  className={`
                    flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all
                    ${active 
                      ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-indigo-500/30' 
                      : 'text-slate-300 hover:bg-white/5 hover:text-white'
                    }
                    ${sidebarCollapsed ? 'justify-center' : ''}
                  `}
                  title={sidebarCollapsed ? item.name : undefined}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {!sidebarCollapsed && <span>{item.name}</span>}
                </Link>
              );
            })}
          </div>
        </div>

        <div className="px-3">
          {!sidebarCollapsed && (
            <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Global Views
            </p>
          )}
          <div className="space-y-1">
            {globalNavigation.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.to);
              
              return (
                <Link
                  key={item.name}
                  to={item.to}
                  className={`
                    flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all
                    ${active 
                      ? 'bg-white/10 text-white' 
                      : 'text-slate-400 hover:bg-white/5 hover:text-slate-300'
                    }
                    ${sidebarCollapsed ? 'justify-center' : ''}
                  `}
                  title={sidebarCollapsed ? item.name : undefined}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {!sidebarCollapsed && <span>{item.name}</span>}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      <div className="border-t border-white/5 p-4">
        <button
          onClick={() => useUIStore.getState().toggleSidebar()}
          className="flex items-center justify-center w-full px-3 py-2 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all"
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <ChevronRight 
            className={`w-5 h-5 transition-transform duration-300 ${sidebarCollapsed ? 'rotate-0' : 'rotate-180'}`} 
          />
        </button>
      </div>
    </aside>
  );
}
