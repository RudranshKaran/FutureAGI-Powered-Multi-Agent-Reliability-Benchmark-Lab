export interface ExperimentConfig {
  architecture: string;
  dataset: string;
  model: string;
  rounds: number;
  temperature: number;
}

export interface ExperimentResult {
  experiment_id: string;
  total_runs: number;
  avg_tokens: number;
  avg_latency_ms: number;
  avg_accuracy: number | null;
  avg_hallucination: number | null;
  avg_coherence: number | null;
  avg_safety: number | null;
}
