import MetricCard from "@/components/dashboard/MetricCard";
import ExperimentsTable from "@/components/dashboard/ExperimentsTable";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const mockMetrics = [
  {
    label: "ACCURACY",
    value: "84%",
    delta: "+9% vs baseline",
    deltaType: "positive" as const,
  },
  {
    label: "HALLUCINATION",
    value: "12%",
    delta: "-5% vs baseline",
    deltaType: "positive" as const,
  },
  {
    label: "TOKENS USED",
    value: "24,521",
    delta: "+15% overhead",
    deltaType: "negative" as const,
  },
  {
    label: "AVG LATENCY",
    value: "1.2s",
    delta: "+0.3s overhead",
    deltaType: "negative" as const,
  },
];

const mockExperiments = [
  {
    id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    architecture: "Two Agent Debate",
    dataset: "arithmetic",
    runs: 10,
    created: "2026-03-04",
  },
  {
    id: "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    architecture: "Single Agent",
    dataset: "arithmetic",
    runs: 10,
    created: "2026-03-04",
  },
  {
    id: "c3d4e5f6-a7b8-9012-cdef-123456789012",
    architecture: "Self Refinement",
    dataset: "commonsense",
    runs: 8,
    created: "2026-03-03",
  },
  {
    id: "d4e5f6a7-b8c9-0123-defa-234567890123",
    architecture: "Two Agent Debate",
    dataset: "commonsense",
    runs: 8,
    created: "2026-03-02",
  },
];

export default function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-foreground mb-1">
          Agent Reliability Lab
        </h1>
        <p className="text-sm text-muted-foreground">
          Multi-agent reasoning reliability benchmarks at a glance.
        </p>
      </div>

      {/* Metric cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {mockMetrics.map((m) => (
          <MetricCard key={m.label} {...m} />
        ))}
      </div>

      {/* Chart placeholder */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Accuracy Comparison Chart
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex h-48 items-center justify-center rounded-md border border-dashed border-border text-sm text-muted-foreground">
            Chart visualization — Coming in Phase 6
          </div>
        </CardContent>
      </Card>

      {/* Experiments table */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Recent Experiments
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ExperimentsTable experiments={mockExperiments} />
        </CardContent>
      </Card>
    </div>
  );
}
