export default function OverviewTab({ service }) {
  return (
    <div className="space-y-6">
      <div className="bg-white/5 rounded-xl p-6 border border-white/5">
        <h3 className="text-lg font-semibold text-slate-50 mb-2">Service Information</h3>
        <p className="text-sm text-slate-400 mb-4">{service.description}</p>
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-300">
          <div>
            <dt className="text-slate-500">Owner</dt>
            <dd className="font-semibold text-slate-200">{service.owner}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Firewall</dt>
            <dd className="font-semibold text-slate-200">{service.firewall}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Created</dt>
            <dd className="font-semibold text-slate-200">{new Date(service.createdAt).toLocaleDateString()}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Last Updated</dt>
            <dd className="font-semibold text-slate-200">{new Date(service.updatedAt).toLocaleDateString()}</dd>
          </div>
        </dl>
      </div>

      <div className="bg-white/5 rounded-xl p-6 border border-white/5">
        <h3 className="text-lg font-semibold text-slate-50 mb-2">Phase 3 Preview</h3>
        <p className="text-sm text-slate-400">
          The detailed overview with network topology, quick actions, and expiration warnings will be implemented in Phase 3
          according to the UI design plan. This placeholder confirms that the routing and layout are ready for upcoming work.
        </p>
      </div>
    </div>
  );
}
