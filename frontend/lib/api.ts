import axios from "axios";
import type {
  ExperimentConfig,
  ExperimentResultsResponse,
  ExperimentStartResponse,
  ExperimentStatus,
} from "@/types/experiment";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function runExperiment(
  config: ExperimentConfig
): Promise<ExperimentStartResponse> {
  const { data } = await api.post<ExperimentStartResponse>(
    "/experiments/run",
    config
  );
  return data;
}

export async function getExperimentStatus(
  experimentId: string
): Promise<ExperimentStatus> {
  const { data } = await api.get<ExperimentStatus>(
    `/experiments/${encodeURIComponent(experimentId)}/status`
  );
  return data;
}

export async function healthCheck(): Promise<{ status: string }> {
  const { data } = await api.get<{ status: string }>("/health");
  return data;
}

export async function getExperimentResults(
  experimentId: string
): Promise<ExperimentResultsResponse> {
  const { data } = await api.get<ExperimentResultsResponse>(
    `/experiments/${encodeURIComponent(experimentId)}/results`
  );
  return data;
}

export default api;
