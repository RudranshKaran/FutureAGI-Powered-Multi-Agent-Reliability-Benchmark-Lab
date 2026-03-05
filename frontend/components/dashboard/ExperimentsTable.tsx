"use client";

import { useRouter } from "next/navigation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Experiment {
  id: string;
  architecture: string;
  dataset: string;
  runs: number;
  created: string;
}

interface ExperimentsTableProps {
  experiments: Experiment[];
}

export default function ExperimentsTable({
  experiments,
}: ExperimentsTableProps) {
  const router = useRouter();

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Experiment ID</TableHead>
          <TableHead>Architecture</TableHead>
          <TableHead>Dataset</TableHead>
          <TableHead className="text-right">Runs</TableHead>
          <TableHead className="text-right">Created</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {experiments.map((exp) => (
          <TableRow
            key={exp.id}
            className="cursor-pointer"
            onClick={() => router.push(`/experiments/${exp.id}`)}
          >
            <TableCell className="font-mono text-xs">
              {exp.id.slice(0, 8)}...
            </TableCell>
            <TableCell>{exp.architecture}</TableCell>
            <TableCell>{exp.dataset}</TableCell>
            <TableCell className="text-right">{exp.runs}</TableCell>
            <TableCell className="text-right text-muted-foreground">
              {exp.created}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
