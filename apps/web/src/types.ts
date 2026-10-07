export type ModelId = "fraud" | "credit" | "spam" | "typo" | "rag";

export type ModelInfo = {
  id: ModelId;
  name: string;
  task: string;
  description: string;
  technology: string[];
  headline_metric: string;
  headline_value: string;
  secondary_metric: string;
  live: boolean;
  data_scope: string;
  repo_path: string;
};

export type Overview = {
  name: string;
  systems: number;
  live_systems: number;
  models: ModelInfo[];
  quality: {
    tests: string;
    ci: boolean;
    dependency_audit: boolean;
    reproducible_metrics: boolean;
  };
};

export type CalibrationRecord = {
  id: number;
  question: string;
  answerable: boolean;
  top_score: number;
};

export type RAGEvaluation = {
  retrieval: {
    total_questions: number;
    answerable_questions: number;
    top_k: number;
    hit_at_1: number;
    hit_at_3: number;
    mrr_at_3: number;
  };
  abstention: {
    threshold: number;
    balanced_accuracy: number;
    answerable_recall: number;
    unanswerable_recall: number;
    embedding_model: string;
    embedding_revision: string;
  };
  calibration_records: CalibrationRecord[];
};
