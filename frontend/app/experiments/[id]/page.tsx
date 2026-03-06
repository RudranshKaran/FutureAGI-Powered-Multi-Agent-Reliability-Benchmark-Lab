"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { getExperimentStatus } from "@/lib/api";
import type { ExperimentStatus } from "@/types/experiment";
import StatusBanner from "@/components/experiments/StatusBanner";
import ProgressBar from "@/components/experiments/ProgressBar";
import MetricsPanel from "@/components/experiments/MetricsPanel";
import LogsPanel from "@/components/experiments/LogsPanel";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

const POLL_INTERVAL = 2000;

export default function ExperimentMonitorPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const experimentId = params.id;

  const [status, setStatus] = useState<ExperimentStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      const data = await getExperimentStatus(experimentId);
      setStatus(data);
      setError(null);

      // Stop polling on terminal states
      if (
        (data.status === "completed" || data.status === "failed") &&
        intervalRef.current
      ) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    } catch {
      setError("Connection lost. Retrying…");
    } finally {
      setLoading(false);
    }
  }, [experimentId]);

  useEffect(() => {
    fetchStatus();
    intervalRef.current = setInterval(fetchStatus, POLL_INTERVAL);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [fetchStatus]);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        <span className="ml-2 text-sm text-muted-foreground">
          Loading experiment…
        </span>
      </div>
    );
  }

  if (!status) {
    return (
      <Card>
        <CardContent className="p-5">
          <p className="text-sm text-destructive">
            Failed to load experiment status.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-foreground mb-1">
          Experiment Monitor
        </h1>
        <p className="text-sm text-muted-foreground">
          Live execution tracking for experiment{" "}
          <span className="font-mono text-foreground">
            {experimentId.slice(0, 8)}…
          </span>
        </p>
      </div>

      {/* Connection error banner */}
      {error && (
        <div className="rounded-md border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-400">
          {error}
        </div>
      )}

      {/* Status Banner */}
      <StatusBanner
        status={status.status}
        architecture={status.architecture}
        dataset={status.dataset}
      />

      {/* Progress Bar */}
      <ProgressBar
        completedRuns={status.completed_runs}
        totalPrompts={status.total_prompts}
        progressPercentage={status.progress_percentage}
      />

      {/* Metrics Counters */}
      <MetricsPanel
        avgTokens={status.avg_tokens}
        avgLatencyMs={status.avg_latency_ms}
      />

      {/* Logs Panel */}
      <LogsPanel logs={status.logs} />

      {/* View Results button — shown when experiment completes */}
      {status.status === "completed" && (
        <Button
          className="w-full"
          onClick={() => router.push(`/experiments/${experimentId}/results`)}
        >
          View Results
        </Button>
      )}
    </div>
  );
}
