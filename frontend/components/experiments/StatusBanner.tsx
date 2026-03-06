"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import type { ExperimentStatus } from "@/types/experiment";

const statusConfig: Record<
  ExperimentStatus["status"],
  { label: string; className: string }
> = {
  pending: {
    label: "Pending",
    className: "bg-muted text-muted-foreground border-muted",
  },
  running: {
    label: "Running",
    className: "bg-primary/15 text-primary border-primary/30",
  },
  completed: {
    label: "Completed",
    className: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
  },
  failed: {
    label: "Failed",
    className: "bg-destructive/15 text-destructive border-destructive/30",
  },
};

interface StatusBannerProps {
  status: ExperimentStatus["status"];
  architecture: string;
  dataset: string;
}

export default function StatusBanner({
  status,
  architecture,
  dataset,
}: StatusBannerProps) {
  const config = statusConfig[status];

  return (
    <Card>
      <CardContent className="flex items-center justify-between p-5">
        <div>
          <h2 className="text-lg font-semibold text-foreground">
            Experiment {config.label}
          </h2>
          <p className="text-sm text-muted-foreground mt-0.5">
            Dataset: <span className="text-foreground">{dataset}</span>
            {" · "}
            Architecture:{" "}
            <span className="text-foreground">{architecture}</span>
          </p>
        </div>
        <Badge className={config.className}>{config.label}</Badge>
      </CardContent>
    </Card>
  );
}
