"use client";

import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const architectures = [
  {
    value: "single_agent",
    label: "Single Agent",
    description: "Baseline single-pass LLM reasoning with no refinement.",
  },
  {
    value: "two_agent_debate",
    label: "Two Agent Debate",
    description:
      "Two agents debate through structured critique rounds, then an aggregator produces the final answer.",
  },
  {
    value: "self_refinement",
    label: "Self Refinement",
    description:
      "A single agent generates an answer, self-critiques, and revises iteratively.",
  },
];

interface ArchitectureSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

export default function ArchitectureSelector({
  value,
  onChange,
}: ArchitectureSelectorProps) {
  const selected = architectures.find((a) => a.value === value);

  return (
    <div className="space-y-3">
      <Label>Architecture</Label>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger>
          <SelectValue placeholder="Select architecture" />
        </SelectTrigger>
        <SelectContent>
          {architectures.map((arch) => (
            <SelectItem key={arch.value} value={arch.value}>
              {arch.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {selected && (
        <p className="text-xs text-muted-foreground">{selected.description}</p>
      )}
    </div>
  );
}
