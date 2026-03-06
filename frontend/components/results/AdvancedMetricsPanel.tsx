"use client";

import MetricCard from "@/components/dashboard/MetricCard";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import type { AdvancedMetrics } from "@/types/experiment";

interface AdvancedMetricsPanelProps {
  metrics: AdvancedMetrics;
}

function convergenceLabel(score: number): string {
  if (score > 0.9) return "Minimal change";
  if (score >= 0.7) return "Refinement";
  return "Significant shift";
}

export default function AdvancedMetricsPanel({
  metrics,
}: AdvancedMetricsPanelProps) {
  const improvementPerToken =
    metrics.improvement_per_token != null
      ? metrics.improvement_per_token.toExponential(2)
      : "N/A";

  const latencyOverhead =
    metrics.latency_overhead_percent != null
      ? `${metrics.latency_overhead_percent.toFixed(1)}%`
      : "N/A";

  const latencyDeltaType: "positive" | "negative" | "neutral" =
    metrics.latency_overhead_percent != null
      ? metrics.latency_overhead_percent > 0
        ? "negative"
        : "positive"
      : "neutral";

  const stabilityScore =
    metrics.stability_score != null
      ? metrics.stability_score.toFixed(2)
      : "N/A";

  const stabilityDeltaType: "positive" | "negative" | "neutral" =
    metrics.stability_score != null
      ? metrics.stability_score >= 0.7
        ? "positive"
        : metrics.stability_score >= 0.4
        ? "neutral"
        : "negative"
      : "neutral";

  const confidenceInterval =
    metrics.confidence_interval != null
      ? `${(metrics.confidence_interval[0] * 100).toFixed(1)}% — ${(metrics.confidence_interval[1] * 100).toFixed(1)}%`
      : "N/A";

  const convergenceScore =
    metrics.convergence_score != null
      ? metrics.convergence_score.toFixed(3)
      : "N/A";

  const convergenceDelta =
    metrics.convergence_score != null
      ? convergenceLabel(metrics.convergence_score)
      : undefined;

  const variance =
    metrics.accuracy_variance != null
      ? metrics.accuracy_variance.toFixed(4)
      : "N/A";

  const varianceSubtext =
    metrics.accuracy_std != null
      ? `σ = ${metrics.accuracy_std.toFixed(4)}`
      : "Requires 2+ experiments";

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-semibold text-foreground">
          Advanced Metrics
        </h3>
        <p className="text-sm text-muted-foreground">
          Research-grade analysis of efficiency, stability, and convergence
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <MetricCard
            label="Improvement / Token"
            value={improvementPerToken}
            subtext={
              metrics.improvement_per_token != null
                ? "accuracy gain per token"
                : "No baseline available"
            }
            deltaType={
              metrics.improvement_per_token != null
                ? metrics.improvement_per_token > 0
                  ? "positive"
                  : "negative"
                : "neutral"
            }
          />
          <MetricCard
            label="Latency Overhead"
            value={latencyOverhead}
            subtext={
              metrics.latency_overhead_percent != null
                ? "vs single-agent"
                : "No baseline available"
            }
            deltaType={latencyDeltaType}
          />
          <MetricCard
            label="Stability Score"
            value={stabilityScore}
            subtext="0 = unstable, 1 = highly stable"
            deltaType={stabilityDeltaType}
          />
          <MetricCard
            label="Confidence Interval"
            value={confidenceInterval}
            subtext={
              metrics.confidence_interval != null
                ? "95% CI for accuracy"
                : "Requires 2+ experiments"
            }
          />
          <MetricCard
            label="Convergence Score"
            value={convergenceScore}
            delta={convergenceDelta}
            subtext={
              metrics.convergence_score == null
                ? "Only for debate/refine"
                : undefined
            }
          />
          <MetricCard
            label="Accuracy Variance"
            value={variance}
            subtext={varianceSubtext}
          />
        </div>
      </CardContent>
    </Card>
  );
}
