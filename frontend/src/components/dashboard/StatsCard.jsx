import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export default function StatsCard({ title, value, change, icon: Icon }) {
  const trend = change > 0 ? 'up' : change < 0 ? 'down' : 'neutral';

  return (
    <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-6 hover:border-white/10 transition-all">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm font-medium text-slate-400">{title}</p>
        {Icon && (
          <div className="p-2 bg-gradient-to-r from-blue-600/20 to-indigo-600/20 rounded-lg">
            <Icon className="w-5 h-5 text-indigo-400" />
          </div>
        )}
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-3xl font-bold text-slate-50 mb-1">{value.toLocaleString()}</p>
          {change !== undefined && (
            <div className="flex items-center gap-1">
              {trend === 'up' && (
                <>
                  <TrendingUp className="w-4 h-4 text-emerald-400" />
                  <span className="text-sm font-medium text-emerald-400">+{Math.abs(change)}</span>
                </>
              )}
              {trend === 'down' && (
                <>
                  <TrendingDown className="w-4 h-4 text-rose-400" />
                  <span className="text-sm font-medium text-rose-400">-{Math.abs(change)}</span>
                </>
              )}
              {trend === 'neutral' && (
                <>
                  <Minus className="w-4 h-4 text-slate-500" />
                  <span className="text-sm font-medium text-slate-500">0</span>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
