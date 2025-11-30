export default function StatusIndicator({ status, size = 'md' }) {
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  const statusColors = {
    healthy: 'bg-emerald-500',
    warning: 'bg-amber-500',
    critical: 'bg-rose-500',
    inactive: 'bg-slate-500',
  };

  return (
    <div
      className={`rounded-full ${sizeClasses[size]} ${statusColors[status]} shadow-lg ${
        status === 'healthy' ? 'shadow-emerald-500/50' : ''
      } ${status === 'warning' ? 'shadow-amber-500/50' : ''} ${
        status === 'critical' ? 'shadow-rose-500/50' : ''
      }`}
      aria-label={`Status: ${status}`}
    />
  );
}
