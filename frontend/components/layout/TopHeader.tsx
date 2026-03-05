"use client";

import { usePathname } from "next/navigation";
import { Badge } from "@/components/ui/badge";

const pageTitles: Record<string, string> = {
  "/": "Dashboard",
  "/experiment": "New Experiment",
  "/experiments": "Experiments",
  "/evaluations": "Evaluations",
  "/logs": "Logs",
  "/settings": "Settings",
};

export default function TopHeader() {
  const pathname = usePathname();
  const title = pageTitles[pathname] ?? "Dashboard";

  return (
    <header className="h-14 shrink-0 border-b border-border bg-card flex items-center justify-between px-6 sticky top-0 z-10">
      <span className="text-sm font-medium text-foreground">{title}</span>
      <div className="flex items-center gap-3">
        <Badge
          variant="outline"
          className="text-xs text-muted-foreground border-border"
        >
          Local
        </Badge>
        <span className="flex items-center gap-1.5 text-xs text-success bg-success/10 px-2 py-1 rounded">
          <span className="h-1.5 w-1.5 rounded-full bg-success" />
          Connected to FutureAGI
        </span>
      </div>
    </header>
  );
}
