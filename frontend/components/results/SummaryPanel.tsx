"use client";

import MetricCard from "@/components/dashboard/MetricCard";
import type {
  ExperimentSummary,
  ArchitectureComparisonItem,
} from "@/types/experiment";

interface SummaryPanelProps {
  summary: ExperimentSummary;
  currentArchitecture: string;
  architectureComparison: ArchitectureComparisonItem[];
}

export default function SummaryPanel({
  summary,
  currentArchitecture,
  architectureComparison,
}: SummaryPanelProps) {
  // Compute delta vs single_agent baseline
  const baseline = architectureComparison.find(
    (a) => a.architecture === "single_agent"
  );
  const current = architectureComparison.find(
    (a) => a.architecture === currentArchitecture
  );

  let accuracyDelta: string | undefined;
  let deltaType: "positive" | "negative" | "neutral" = "neutral";

  if (
    baseline &&
    current &&
    baseline.architecture !== current.architecture
  ) {
    const diff = ((current.accuracy - baseline.accuracy) * 100).toFixed(1);
    const sign = Number(diff) >= 0 ? "+" : "";
    accuracyDelta = `${sign}${diff}% vs baseline`;
    deltaType = Number(diff) > 0 ? "positive" : Number(diff) < 0 ? "negative" : "neutral";
  }

  const accuracy = summary.avg_accuracy != null
    ? `${(summary.avg_accuracy * 100).toFixed(1)}%`
    : "N/A";

  const hallucination = summary.avg_hallucination != null
    ? `${(summary.avg_hallucination * 100).toFixed(1)}%`
    : "N/A";

  return (
    <div className="grid grid-cols-4 gap-6">
      <MetricCard
        label="Accuracy"
        value={accuracy}
        delta={accuracyDelta}
        deltaType={deltaType}
      />
      <MetricCard
        label="Hallucination Rate"
        value={hallucination}
        deltaType="negative"
      />
      <MetricCard
        label="Avg Tokens"
        value={summary.avg_tokens.toFixed(0)}
        subtext="per prompt"
      />
      <MetricCard
        label="Avg Latency"
        value={`${summary.avg_latency_ms.toFixed(0)}ms`}
        subtext="per prompt"
      />
    </div>
  );
}
