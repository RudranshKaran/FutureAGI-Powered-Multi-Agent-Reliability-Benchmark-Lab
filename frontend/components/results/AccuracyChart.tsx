"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import type { ArchitectureComparisonItem } from "@/types/experiment";

interface AccuracyChartProps {
  data: ArchitectureComparisonItem[];
  currentArchitecture: string;
}

const ACTIVE_COLOR = "#6366F1";
const MUTED_COLOR = "#4B5563";

const labels: Record<string, string> = {
  single_agent: "Single Agent",
  two_agent_debate: "Two-Agent Debate",
  self_refinement: "Self Refine",
};

export default function AccuracyChart({
  data,
  currentArchitecture,
}: AccuracyChartProps) {
  const chartData = data.map((d) => ({
    ...d,
    label: labels[d.architecture] ?? d.architecture,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">
          Accuracy Comparison by Architecture
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
            <XAxis
              dataKey="label"
              tick={{ fill: "#9CA3AF", fontSize: 12 }}
              axisLine={{ stroke: "#1F2937" }}
              tickLine={false}
            />
            <YAxis
              domain={[0, 1]}
              tick={{ fill: "#9CA3AF", fontSize: 12 }}
              axisLine={{ stroke: "#1F2937" }}
              tickLine={false}
              tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#111827",
                border: "1px solid #1F2937",
                borderRadius: 8,
                color: "#F3F4F6",
                fontSize: 12,
              }}
              formatter={(value) => [`${(Number(value) * 100).toFixed(1)}%`, "Accuracy"]}
            />
            <Bar dataKey="accuracy" radius={[4, 4, 0, 0]} maxBarSize={64}>
              {chartData.map((entry, i) => (
                <Cell
                  key={i}
                  fill={
                    entry.architecture === currentArchitecture
                      ? ACTIVE_COLOR
                      : MUTED_COLOR
                  }
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
