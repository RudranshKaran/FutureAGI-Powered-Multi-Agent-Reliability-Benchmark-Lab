import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  label: string;
  value: string;
  delta?: string;
  subtext?: string;
  deltaType?: "positive" | "negative" | "neutral";
}

export default function MetricCard({
  label,
  value,
  delta,
  subtext,
  deltaType = "neutral",
}: MetricCardProps) {
  return (
    <Card>
      <CardContent className="p-5">
        <p className="text-xs font-medium text-muted-foreground tracking-wide uppercase">
          {label}
        </p>
        <p className="text-3xl font-bold text-foreground mt-1">{value}</p>
        {delta && (
          <p
            className={cn(
              "text-xs mt-1",
              deltaType === "positive" && "text-success",
              deltaType === "negative" && "text-error",
              deltaType === "neutral" && "text-muted-foreground"
            )}
          >
            {delta}
          </p>
        )}
        {subtext && !delta && (
          <p className="text-xs text-muted-foreground mt-1">{subtext}</p>
        )}
      </CardContent>
    </Card>
  );
}
