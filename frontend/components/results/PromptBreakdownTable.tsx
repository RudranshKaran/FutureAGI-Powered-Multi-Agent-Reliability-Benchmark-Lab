"use client";

import { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { ChevronDown, ChevronUp } from "lucide-react";
import type { PromptBreakdown } from "@/types/experiment";

interface PromptBreakdownTableProps {
  data: PromptBreakdown[];
}

export default function PromptBreakdownTable({
  data,
}: PromptBreakdownTableProps) {
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());

  const toggleRow = (index: number) => {
    setExpandedRows((prev) => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">
          Prompt-Level Breakdown
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="pl-6">Prompt</TableHead>
              <TableHead className="text-right">Accuracy</TableHead>
              <TableHead className="text-right">Tokens</TableHead>
              <TableHead className="text-right">Latency</TableHead>
              <TableHead className="text-right pr-6">Details</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((row, i) => {
              const isExpanded = expandedRows.has(i);
              return (
                <ExpandableRow
                  key={i}
                  row={row}
                  index={i}
                  isExpanded={isExpanded}
                  onToggle={() => toggleRow(i)}
                />
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}

function ExpandableRow({
  row,
  index,
  isExpanded,
  onToggle,
}: {
  row: PromptBreakdown;
  index: number;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  return (
    <>
      <TableRow className="hover:bg-muted/50 transition-colors">
        <TableCell className="pl-6 max-w-xs truncate font-mono text-xs">
          {row.prompt.length > 80
            ? `${row.prompt.slice(0, 80)}…`
            : row.prompt}
        </TableCell>
        <TableCell className="text-right tabular-nums">
          {row.accuracy != null
            ? `${(row.accuracy * 100).toFixed(1)}%`
            : "N/A"}
        </TableCell>
        <TableCell className="text-right tabular-nums">{row.tokens}</TableCell>
        <TableCell className="text-right tabular-nums">
          {row.latency_ms.toFixed(0)}ms
        </TableCell>
        <TableCell className="text-right pr-6">
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggle}
            className="text-xs"
          >
            {isExpanded ? (
              <>
                Hide <ChevronUp className="ml-1 h-3 w-3" />
              </>
            ) : (
              <>
                View <ChevronDown className="ml-1 h-3 w-3" />
              </>
            )}
          </Button>
        </TableCell>
      </TableRow>

      {isExpanded && (
        <TableRow>
          <TableCell colSpan={5} className="bg-muted/30 px-6 py-4">
            <div className="space-y-4 text-sm">
              {/* Prompt */}
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                  Prompt
                </p>
                <p className="font-mono text-xs text-foreground whitespace-pre-wrap">
                  {row.prompt}
                </p>
              </div>

              {/* Final Output */}
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                  Final Output
                </p>
                <p className="font-mono text-xs text-foreground whitespace-pre-wrap">
                  {row.final_output ?? "—"}
                </p>
              </div>

              {/* Debate Traces */}
              {row.debate_traces.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
                    Agent Reasoning Steps
                  </p>
                  <div className="space-y-2">
                    {row.debate_traces.map((trace, j) => (
                      <div
                        key={j}
                        className="rounded-md border border-border bg-card p-3"
                      >
                        <div className="flex items-center gap-3 mb-1 text-xs text-muted-foreground">
                          <span className="font-semibold text-foreground">
                            {trace.agent_role}
                          </span>
                          <span>Turn {trace.turn_number}</span>
                          <span>{trace.tokens} tokens</span>
                          <span>{trace.latency_ms.toFixed(0)}ms</span>
                        </div>
                        <p className="font-mono text-xs text-foreground/80 whitespace-pre-wrap">
                          {trace.response}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* FutureAGI Scores */}
              {row.accuracy != null && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                    FutureAGI Scores
                  </p>
                  <div className="flex gap-4 text-xs">
                    <span>
                      Accuracy:{" "}
                      <span className="font-semibold text-foreground">
                        {(row.accuracy * 100).toFixed(1)}%
                      </span>
                    </span>
                  </div>
                </div>
              )}
            </div>
          </TableCell>
        </TableRow>
      )}
    </>
  );
}
