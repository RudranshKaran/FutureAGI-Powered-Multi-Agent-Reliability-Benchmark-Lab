"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getExperimentResults } from "@/lib/api";
import type { ExperimentResultsResponse } from "@/types/experiment";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import SummaryPanel from "@/components/results/SummaryPanel";
import AccuracyChart from "@/components/results/AccuracyChart";
import TokenAccuracyChart from "@/components/results/TokenAccuracyChart";
import RoundsImprovementChart from "@/components/results/RoundsImprovementChart";
import PromptBreakdownTable from "@/components/results/PromptBreakdownTable";

const archLabels: Record<string, string> = {
  single_agent: "Single Agent",
  two_agent_debate: "Two-Agent Debate",
  self_refinement: "Self Refine",
};

export default function ExperimentResultsPage() {
  const params = useParams<{ id: string }>();
  const experimentId = params.id;

  const [results, setResults] = useState<ExperimentResultsResponse | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchResults() {
      try {
        const data = await getExperimentResults(experimentId);
        if (!cancelled) {
          setResults(data);
          setError(null);
        }
      } catch (err: unknown) {
        if (!cancelled) {
          const message =
            err instanceof Error ? err.message : "Failed to load results";
          setError(message);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchResults();
    return () => {
      cancelled = true;
    };
  }, [experimentId]);

  if (loading) return <ResultsSkeleton />;

  if (error || !results) {
    return (
      <Card>
        <CardContent className="p-5">
          <p className="text-sm text-destructive">
            {error ?? "Failed to load experiment results."}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold text-foreground mb-1">
          Experiment Results
        </h1>
        <div className="flex items-center gap-3 text-sm text-muted-foreground">
          <span className="font-mono text-foreground">
            {experimentId.slice(0, 8)}…
          </span>
          <Badge variant="secondary">
            {archLabels[results.architecture] ?? results.architecture}
          </Badge>
          <Badge variant="outline">{results.dataset}</Badge>
          <span>{results.rounds} round{results.rounds !== 1 ? "s" : ""}</span>
        </div>
      </div>

      {/* Summary Metrics */}
      <SummaryPanel
        summary={results.summary}
        currentArchitecture={results.architecture}
        architectureComparison={results.architecture_comparison}
      />

      {/* Accuracy Comparison */}
      {results.architecture_comparison.length > 0 && (
        <AccuracyChart
          data={results.architecture_comparison}
          currentArchitecture={results.architecture}
        />
      )}

      {/* Token vs Accuracy */}
      {results.token_accuracy_points.length > 0 && (
        <TokenAccuracyChart data={results.token_accuracy_points} />
      )}

      {/* Debate Rounds Improvement */}
      {results.round_improvement.length > 0 && (
        <RoundsImprovementChart data={results.round_improvement} />
      )}

      {/* Prompt Breakdown */}
      {results.prompt_breakdown.length > 0 && (
        <PromptBreakdownTable data={results.prompt_breakdown} />
      )}
    </div>
  );
}

function ResultsSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header skeleton */}
      <div>
        <Skeleton className="h-8 w-64 mb-2" />
        <Skeleton className="h-4 w-96" />
      </div>

      {/* Summary cards skeleton */}
      <div className="grid grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i}>
            <CardContent className="p-5">
              <Skeleton className="h-3 w-20 mb-2" />
              <Skeleton className="h-8 w-16" />
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Chart skeletons */}
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-[300px] w-full" />
          </CardContent>
        </Card>
      ))}

      {/* Table skeleton */}
      <Card>
        <CardHeader>
          <Skeleton className="h-4 w-40" />
        </CardHeader>
        <CardContent className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-10 w-full" />
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
