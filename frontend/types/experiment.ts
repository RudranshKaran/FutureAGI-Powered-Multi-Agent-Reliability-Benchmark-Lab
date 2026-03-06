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

export interface ExperimentStartResponse {
  experiment_id: string;
}

export interface ExperimentStatus {
  experiment_id: string;
  status: "pending" | "running" | "completed" | "failed";
  architecture: string;
  dataset: string;
  total_prompts: number;
  completed_runs: number;
  progress_percentage: number;
  avg_tokens: number;
  avg_latency_ms: number;
  logs: string[];
}
