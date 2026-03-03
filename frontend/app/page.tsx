export default function Home() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-primary mb-1">
        Agent Reliability Lab
      </h1>
      <p className="text-sm text-secondary mb-8">Dashboard Placeholder</p>

      {/* Placeholder metric cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'ACCURACY', value: '—', delta: '' },
          { label: 'HALLUCINATION', value: '—', delta: '' },
          { label: 'TOKENS USED', value: '—', delta: '' },
          { label: 'AVG LATENCY', value: '—', delta: '' },
        ].map((card) => (
          <div
            key={card.label}
            className="rounded-lg border border-border bg-card p-5"
          >
            <p className="text-xs font-medium text-secondary tracking-wide uppercase">
              {card.label}
            </p>
            <p className="text-3xl font-bold text-primary mt-1">{card.value}</p>
            <p className="text-xs text-secondary mt-1">
              {card.delta || 'No data yet'}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
