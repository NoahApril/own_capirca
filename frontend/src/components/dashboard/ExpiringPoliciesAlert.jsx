import { AlertTriangle, Timer } from 'lucide-react';

export default function ExpiringPoliciesAlert({ policies }) {
  return (
    <div className="bg-gradient-to-r from-rose-500/10 via-amber-500/10 to-transparent border border-rose-500/20 rounded-xl shadow-xl p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-rose-500/20 text-rose-400">
          <AlertTriangle className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-slate-50">Policies expiring soon</h2>
          <p className="text-sm text-slate-300">{policies.length} policies require attention within 72h</p>
        </div>
      </div>

      <div className="space-y-3">
        {policies.map((policy) => (
          <div key={policy.id} className="bg-white/5 rounded-lg px-4 py-3 flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-slate-200">{policy.serviceName}</p>
              <p className="text-xs text-slate-400">{policy.source.join(', ')} → {policy.destination.join(', ')}</p>
            </div>
            <div className="flex items-center gap-2 text-amber-300 text-xs font-semibold">
              <Timer className="w-4 h-4" />
              <span>{new Date(policy.expiresAt).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
