"use client";

import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const datasets = [
  { value: "arithmetic", label: "Arithmetic" },
  { value: "reasoning", label: "Reasoning" },
  { value: "factual_qa", label: "Factual QA" },
];

interface DatasetSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

export default function DatasetSelector({
  value,
  onChange,
}: DatasetSelectorProps) {
  return (
    <div className="space-y-3">
      <Label>Dataset</Label>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger>
          <SelectValue placeholder="Select dataset" />
        </SelectTrigger>
        <SelectContent>
          {datasets.map((d) => (
            <SelectItem key={d.value} value={d.value}>
              {d.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
