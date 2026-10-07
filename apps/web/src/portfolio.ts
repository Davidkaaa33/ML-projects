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
  surname: "Danielian",
  role: "Machine Learning Engineer / Data Scientist",
  summary:
    "I build machine learning systems that are evaluated, testable and deployable — from retrieval and NLP pipelines to APIs and containerized inference.",
  github: "https://github.com/Davidkaaa33",
  linkedin: "", // TODO: add LinkedIn URL.
  resume: "/David_Danielian_CV.html",
  email: "d.danielian@innopolis.university",
  education:
    "Innopolis University, BSc in Data Analysis and Artificial Intelligence, 2025–2028, GPA 4.9/5.0",
  location: "Innopolis, Russia",
  currentStatus: "Second-year BSc student, full-tuition scholarship",
  targetRoles: ["Machine Learning Engineer", "Data Scientist"] as string[]
};

export const profileName = [profile.firstName, profile.surname]
  .filter(Boolean)
  .join(" ");

export const featuredProjects: FeaturedProject[] = [
  {
    id: "avito",
    title: "Avito Candidate Retrieval",
    description:
      "Hybrid candidate retrieval for service search, combining lexical and semantic signals under a query-disjoint evaluation setup.",
    problem:
      "Generate a high-recall set of relevant service listings for each search query.",
    approach:
      "BM25 and BGE-M3 retrieval are combined with geographic, microcategory and query-history signals through weighted reciprocal-rank fusion.",
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
      "A single deployable application that exposes five independent ML systems through one FastAPI service and one React interface.",
    problem:
      "Turn separate ML projects into one deployable product without hiding project-specific evaluation boundaries.",
    approach:
      "The service reuses each project’s original inference logic while keeping model-specific evaluation artifacts and API contracts explicit.",
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
      "Local retrieval-augmented generation with citation-aware answers, retrieval evaluation and abstention on unsupported questions.",
    problem:
      "Answer questions from a local document corpus while surfacing retrieval quality and unsupported-query behavior.",
    approach:
      "SentenceTransformer embeddings and FAISS retrieval feed an optional local Qwen/Ollama generation path with explicit source citations.",
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
