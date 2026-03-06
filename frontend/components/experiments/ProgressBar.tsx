"use client";

import { Card, CardContent } from "@/components/ui/card";

interface ProgressBarProps {
  completedRuns: number;
  totalPrompts: number;
  progressPercentage: number;
}

export default function ProgressBar({
  completedRuns,
  totalPrompts,
  progressPercentage,
}: ProgressBarProps) {
  return (
    <Card>
      <CardContent className="p-5 space-y-3">
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">Progress</span>
          <span className="font-medium text-foreground">
            {completedRuns} / {totalPrompts} prompts completed
          </span>
        </div>
        <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
            style={{ width: `${Math.min(progressPercentage, 100)}%` }}
          />
        </div>
        <p className="text-xs text-muted-foreground text-right">
          {progressPercentage.toFixed(1)}%
        </p>
      </CardContent>
    </Card>
  );
}
