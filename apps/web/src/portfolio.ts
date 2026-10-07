export type FeaturedProject = {
  id: string;
  title: string;
  label?: string;
  description: string;
  problem: string;
  approach: string;
  metrics: Array<{ label: string; value: string }>;
  technologies: string[];
  engineering: string[];
  sourceUrl?: string;
  liveUrl?: string;
};

export const profile = {
  firstName: "David",
  surname: "", // TODO: add surname.
  role: "Machine Learning Engineer / Data Scientist",
  summary:
    "I build evaluated machine learning systems — from classical ML and retrieval pipelines to APIs, Dockerized inference and production-oriented evaluation.",
  github: "https://github.com/Davidkaaa33",
  linkedin: "", // TODO: add LinkedIn URL.
  resume: "", // TODO: add public resume URL.
  email: "", // TODO: add preferred contact email.
  education: "", // TODO: add education.
  location: "", // TODO: add location if you want it public.
  currentStatus: "", // TODO: add current status.
  targetRoles: [] as string[] // TODO: add target roles if you want them shown.
};

export const profileName = [profile.firstName, profile.surname]
  .filter(Boolean)
  .join(" ");

export const featuredProjects: FeaturedProject[] = [
  {
    id: "avito",
    title: "Avito Candidate Retrieval",
    label: "Flagship",
    description: "Hybrid lexical + semantic candidate retrieval for service search.",
    problem:
      "Generate a high-recall set of relevant service listings for each search query.",
    approach:
      "BM25 and BGE-M3 retrieval combined with geographic, microcategory and query-history signals through weighted reciprocal-rank fusion.",
    metrics: [{ label: "Recall@50", value: "0.8316" }],
    technologies: ["BM25", "BGE-M3", "Retrieval", "Ranking", "NLP"],
    engineering: [
      "query-disjoint validation",
      "deterministic asset builders",
      "submitted artifact hash verification"
    ],
    sourceUrl: "https://github.com/Davidkaaa33/avito-ds-bootcamp-2026-solution"
  },
  {
    id: "systems-lab",
    title: "ML Systems Lab",
    description:
      "Five independently evaluated ML systems behind a unified FastAPI service with a React interface.",
    problem:
      "Turn separate ML projects into one deployable product without hiding project-specific evaluation boundaries.",
    approach:
      "A unified inference layer adapts the existing model code while React provides interactive controls, evaluation views and API inspection.",
    metrics: [{ label: "Systems", value: "5" }],
    technologies: ["React", "Vite", "FastAPI", "Docker", "pytest", "GitHub Actions"],
    engineering: [
      "typed API contracts",
      "container smoke tests",
      "committed evaluation artifacts"
    ],
    sourceUrl: "https://github.com/Davidkaaa33/ML-projects",
    liveUrl: "#lab"
  },
  {
    id: "knowledge-assistant",
    title: "Knowledge Assistant",
    description:
      "Local retrieval-augmented generation with citations, evaluation and calibrated abstention.",
    problem:
      "Answer questions from a local document corpus while surfacing retrieval quality and unsupported-query behavior.",
    approach:
      "SentenceTransformer embeddings and FAISS retrieval feed an optional local Qwen/Ollama generation path with citation-aware responses.",
    metrics: [
      { label: "Hit@1", value: "81.82%" },
      { label: "Hit@3", value: "100%" },
      { label: "MRR@3", value: "0.9091" }
    ],
    technologies: ["SentenceTransformers", "FAISS", "RAG", "FastAPI", "Qwen / Ollama"],
    engineering: [
      "pinned embedding revision",
      "calibrated abstention",
      "semantic metric-drift gate"
    ],
    sourceUrl:
      "https://github.com/Davidkaaa33/ML-projects/tree/main/llm-knowledge-base-assistant",
    liveUrl: "#lab"
  }
];

export const capabilities = [
  {
    title: "Machine Learning",
    items: [
      "scikit-learn",
      "model evaluation",
      "feature engineering",
      "threshold calibration",
      "imbalanced classification"
    ]
  },
  {
    title: "NLP / Retrieval",
    items: ["SentenceTransformers", "FAISS", "BM25", "embeddings", "RAG"]
  },
  {
    title: "Backend / Serving",
    items: ["FastAPI", "REST APIs", "Docker", "model inference"]
  },
  {
    title: "Quality / Reproducibility",
    items: [
      "pytest",
      "Ruff",
      "GitHub Actions",
      "dependency auditing",
      "committed evaluation artifacts"
    ]
  }
] as const;
