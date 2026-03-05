import axios from "axios";
import type { ExperimentConfig, ExperimentResult } from "@/types/experiment";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function runExperiment(
  config: ExperimentConfig
): Promise<ExperimentResult> {
  const { data } = await api.post<ExperimentResult>(
    "/experiments/run",
    config
  );
  return data;
}

export async function healthCheck(): Promise<{ status: string }> {
  const { data } = await api.get<{ status: string }>("/health");
  return data;
}

export default api;
