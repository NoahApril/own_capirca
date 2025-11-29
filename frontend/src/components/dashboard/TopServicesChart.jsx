export default function TopServicesChart({ services }) {
  if (!services || services.length === 0) {
    return null;
  }

  const maxCount = Math.max(...services.map((s) => s.resourceCount));

  return (
    <div className="bg-slate-800/40 backdrop-blur-md border border-white/5 rounded-xl shadow-xl p-6">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-50">Top Services by Resources</h2>
        <p className="text-sm text-slate-400">Services with highest resource count</p>
      </div>

      <div className="space-y-4">
        {services.map((service, index) => {
          const percentage = (service.resourceCount / maxCount) * 100;
          
          return (
            <div key={service.serviceId}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <span className="text-sm font-semibold text-slate-500">#{index + 1}</span>
                  <span className="text-sm font-medium text-slate-200">{service.serviceName}</span>
                </div>
                <span className="text-sm font-semibold text-slate-300">{service.resourceCount}</span>
              </div>
              <div className="h-2 bg-slate-950/50 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full transition-all duration-500"
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
