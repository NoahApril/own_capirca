export default function ServiceBadge({ shortName, status }) {
  const statusColors = {
    healthy: 'text-emerald-300 border-emerald-500/30 bg-emerald-500/5',
    warning: 'text-amber-300 border-amber-500/30 bg-amber-500/5',
    critical: 'text-rose-300 border-rose-500/30 bg-rose-500/5',
  };

  return (
    <span
      className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide border ${statusColors[status]}`}
    >
      {shortName}
    </span>
  );
}
