import { Search, Bell, Settings, User, Moon, Sun } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export default function Header() {
  const theme = useUIStore((state) => state.theme);
  const toggleTheme = useUIStore((state) => state.toggleTheme);

  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur-md border-b border-white/5 flex items-center justify-between px-6 z-10">
      <div className="flex items-center flex-1 max-w-2xl">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search services, hosts, policies..."
            className="w-full pl-10 pr-4 py-2 bg-slate-950/50 border border-white/10 rounded-lg text-slate-200 placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          />
        </div>
      </div>

      <div className="flex items-center gap-3 ml-6">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </button>

        <button
          className="p-2 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all relative"
          aria-label="Notifications"
        >
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full"></span>
        </button>

        <button
          className="p-2 rounded-lg text-slate-400 hover:bg-white/5 hover:text-white transition-all"
          aria-label="Settings"
        >
          <Settings className="w-5 h-5" />
        </button>

        <div className="h-8 w-px bg-white/10"></div>

        <button className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/5 transition-all">
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
          <span className="text-sm font-medium text-slate-200">Admin</span>
        </button>
      </div>
    </header>
  );
}
