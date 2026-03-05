"use client";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const models = [
  { value: "gpt-4o", label: "GPT-4o" },
  { value: "gpt-4o-mini", label: "GPT-4o Mini" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
];

interface ModelConfigFormProps {
  model: string;
  temperature: number;
  maxTokens: number;
  onModelChange: (value: string) => void;
  onTemperatureChange: (value: number) => void;
  onMaxTokensChange: (value: number) => void;
}

export default function ModelConfigForm({
  model,
  temperature,
  maxTokens,
  onModelChange,
  onTemperatureChange,
  onMaxTokensChange,
}: ModelConfigFormProps) {
  return (
    <div className="space-y-5">
      {/* Model */}
      <div className="space-y-3">
        <Label>Model</Label>
        <Select value={model} onValueChange={onModelChange}>
          <SelectTrigger>
            <SelectValue placeholder="Select model" />
          </SelectTrigger>
          <SelectContent>
            {models.map((m) => (
              <SelectItem key={m.value} value={m.value}>
                {m.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Temperature */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <Label>Temperature</Label>
          <span className="text-sm font-medium text-foreground">
            {temperature.toFixed(1)}
          </span>
        </div>
        <Slider
          min={0}
          max={2}
          step={0.1}
          value={[temperature]}
          onValueChange={([v]) => onTemperatureChange(v)}
        />
      </div>

      {/* Max Tokens */}
      <div className="space-y-3">
        <Label>Max Tokens</Label>
        <Input
          type="number"
          min={1}
          max={16384}
          value={maxTokens}
          onChange={(e) => onMaxTokensChange(Number(e.target.value))}
        />
      </div>
    </div>
  );
}
