"use client";

import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import type { TokenAccuracyPoint } from "@/types/experiment";

interface TokenAccuracyChartProps {
  data: TokenAccuracyPoint[];
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload }: any) {
  if (!active || !payload?.length) return null;
  const point = payload[0].payload as TokenAccuracyPoint & { index: number };
  return (
    <div className="rounded-md border border-border bg-card px-3 py-2 text-xs text-foreground shadow-md">
      <p>Prompt #{point.index + 1}</p>
      <p>Tokens: {point.tokens}</p>
      <p>Accuracy: {(point.accuracy * 100).toFixed(1)}%</p>
    </div>
  );
}

export default function TokenAccuracyChart({ data }: TokenAccuracyChartProps) {
  const chartData = data.map((d, i) => ({ ...d, index: i }));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">
          Token Usage vs Accuracy
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
            <XAxis
              dataKey="tokens"
              type="number"
              name="Tokens"
              tick={{ fill: "#9CA3AF", fontSize: 12 }}
              axisLine={{ stroke: "#1F2937" }}
              tickLine={false}
              label={{
                value: "Tokens",
                position: "insideBottom",
                offset: -4,
                fill: "#9CA3AF",
                fontSize: 12,
              }}
            />
            <YAxis
              dataKey="accuracy"
              type="number"
              name="Accuracy"
              domain={[0, 1]}
              tick={{ fill: "#9CA3AF", fontSize: 12 }}
              axisLine={{ stroke: "#1F2937" }}
              tickLine={false}
              tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Scatter data={chartData} fill="#6366F1" />
          </ScatterChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
