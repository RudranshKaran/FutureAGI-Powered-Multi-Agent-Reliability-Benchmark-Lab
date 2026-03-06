"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import type { RoundImprovement } from "@/types/experiment";

interface RoundsImprovementChartProps {
  data: RoundImprovement[];
}

export default function RoundsImprovementChart({
  data,
}: RoundsImprovementChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">
          Debate Rounds vs Accuracy Improvement
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
            <XAxis
              dataKey="rounds"
              type="number"
              domain={["dataMin", "dataMax"]}
              allowDecimals={false}
              tick={{ fill: "#9CA3AF", fontSize: 12 }}
              axisLine={{ stroke: "#1F2937" }}
              tickLine={false}
              label={{
                value: "Debate Rounds",
                position: "insideBottom",
                offset: -4,
                fill: "#9CA3AF",
                fontSize: 12,
              }}
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
              formatter={(value) => [
                `${(Number(value) * 100).toFixed(1)}%`,
                "Accuracy",
              ]}
              labelFormatter={(label) => `Round ${label}`}
            />
            <Line
              type="monotone"
              dataKey="accuracy"
              stroke="#6366F1"
              strokeWidth={2}
              dot={{ fill: "#6366F1", r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
