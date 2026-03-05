"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import ArchitectureSelector from "@/components/experiment/ArchitectureSelector";
import DebateRoundsSlider from "@/components/experiment/DebateRoundsSlider";
import DatasetSelector from "@/components/experiment/DatasetSelector";
import ModelConfigForm from "@/components/experiment/ModelConfigForm";
import { runExperiment } from "@/lib/api";
import { Loader2 } from "lucide-react";

export default function ExperimentPage() {
  const router = useRouter();

  const [architecture, setArchitecture] = useState("single_agent");
  const [rounds, setRounds] = useState(2);
  const [dataset, setDataset] = useState("arithmetic");
  const [model, setModel] = useState("gpt-4o");
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(1024);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const showRounds = architecture === "two_agent_debate";

  async function handleRun() {
    setError(null);
    setLoading(true);

    try {
      const result = await runExperiment({
        architecture,
        dataset,
        model,
        rounds: showRounds ? rounds : 1,
        temperature,
      });
      router.push(`/experiments/${result.experiment_id}`);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Experiment failed. Check backend connection.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-foreground mb-1">
          New Experiment
        </h1>
        <p className="text-sm text-muted-foreground">
          Configure and launch a reliability benchmark run.
        </p>
      </div>

      {/* Architecture */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">Architecture</CardTitle>
        </CardHeader>
        <CardContent>
          <ArchitectureSelector
            value={architecture}
            onChange={setArchitecture}
          />
        </CardContent>
      </Card>

      {/* Debate Rounds — conditional */}
      {showRounds && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium">
              Execution Settings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <DebateRoundsSlider value={rounds} onChange={setRounds} />
          </CardContent>
        </Card>
      )}

      {/* Model Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Model Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ModelConfigForm
            model={model}
            temperature={temperature}
            maxTokens={maxTokens}
            onModelChange={setModel}
            onTemperatureChange={setTemperature}
            onMaxTokensChange={setMaxTokens}
          />
        </CardContent>
      </Card>

      {/* Dataset Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Dataset Selection
          </CardTitle>
        </CardHeader>
        <CardContent>
          <DatasetSelector value={dataset} onChange={setDataset} />
        </CardContent>
      </Card>

      <Separator />

      {/* Error message */}
      {error && (
        <div className="rounded-md border border-error/30 bg-error/10 px-4 py-3 text-sm text-error">
          {error}
        </div>
      )}

      {/* Run button */}
      <Button
        className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold"
        size="lg"
        onClick={handleRun}
        disabled={loading}
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Running Experiment…
          </>
        ) : (
          "Run Experiment"
        )}
      </Button>
    </div>
  );
}
