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

// ---------------------------------------------------------------------------
// Experiment results / analytics types
// ---------------------------------------------------------------------------

export interface DebateTraceEntry {
  agent_role: string;
  turn_number: number;
  response: string;
  tokens: number;
  latency_ms: number;
}

export interface PromptBreakdown {
  prompt: string;
  final_output: string | null;
  accuracy: number | null;
  tokens: number;
  latency_ms: number;
  debate_traces: DebateTraceEntry[];
}

export interface ArchitectureComparisonItem {
  architecture: string;
  accuracy: number;
}

export interface TokenAccuracyPoint {
  tokens: number;
  accuracy: number;
}

export interface RoundImprovement {
  rounds: number;
  accuracy: number;
}

export interface ExperimentSummary {
  avg_accuracy: number | null;
  avg_hallucination: number | null;
  avg_tokens: number;
  avg_latency_ms: number;
}

export interface AdvancedMetrics {
  improvement_per_token: number | null;
  latency_overhead_percent: number | null;
  convergence_score: number | null;
  accuracy_variance: number | null;
  accuracy_std: number | null;
  accuracy_mean: number | null;
  confidence_interval: [number, number] | null;
  stability_score: number | null;
}

export interface ConvergenceTurn {
  turn: number;
  similarity: number;
}

export interface ExperimentResultsResponse {
  experiment_id: string;
  architecture: string;
  dataset: string;
  rounds: number;
  summary: ExperimentSummary;
  architecture_comparison: ArchitectureComparisonItem[];
  token_accuracy_points: TokenAccuracyPoint[];
  round_improvement: RoundImprovement[];
  prompt_breakdown: PromptBreakdown[];
  advanced_metrics: AdvancedMetrics | null;
  convergence_turns: ConvergenceTurn[];
}
