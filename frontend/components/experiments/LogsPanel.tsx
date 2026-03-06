"use client";

import { useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface LogsPanelProps {
  logs: string[];
}

export default function LogsPanel({ logs }: LogsPanelProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium">Execution Logs</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-80 overflow-y-auto rounded-md border border-border bg-background p-4 font-mono text-xs leading-relaxed">
          {logs.length === 0 ? (
            <p className="text-muted-foreground">
              Waiting for execution logs…
            </p>
          ) : (
            logs.map((entry, i) => (
              <div key={i} className="py-1 border-b border-border/50 last:border-0">
                <span className="text-muted-foreground whitespace-pre-wrap">
                  {entry}
                </span>
              </div>
            ))
          )}
          <div ref={bottomRef} />
        </div>
      </CardContent>
    </Card>
  );
}
