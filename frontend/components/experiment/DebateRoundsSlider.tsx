"use client";

import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";

interface DebateRoundsSliderProps {
  value: number;
  onChange: (value: number) => void;
}

export default function DebateRoundsSlider({
  value,
  onChange,
}: DebateRoundsSliderProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <Label>Debate Rounds</Label>
        <span className="text-sm font-medium text-foreground">{value}</span>
      </div>
      <Slider
        min={1}
        max={5}
        step={1}
        value={[value]}
        onValueChange={([v]) => onChange(v)}
      />
      <p className="text-xs text-muted-foreground">
        Number of critique-revision rounds between agents.
      </p>
    </div>
  );
}
