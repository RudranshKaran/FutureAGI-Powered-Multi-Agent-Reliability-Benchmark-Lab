"use client";

import { Card, CardContent } from "@/components/ui/card";

interface MetricsPanelProps {
  avgTokens: number;
  avgLatencyMs: number;
}

export default function MetricsPanel({
  avgTokens,
  avgLatencyMs,
}: MetricsPanelProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <Card>
        <CardContent className="p-5">
          <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">
            Average Tokens per Run
          </p>
          <p className="text-3xl font-bold text-foreground mt-1">
            {Math.round(avgTokens)}
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-5">
          <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">
            Average Latency per Run
          </p>
          <p className="text-3xl font-bold text-foreground mt-1">
            {Math.round(avgLatencyMs)}{" "}
            <span className="text-base font-normal text-muted-foreground">
              ms
            </span>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
