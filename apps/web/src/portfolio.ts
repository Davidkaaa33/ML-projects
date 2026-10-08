export type FeaturedProject = {
  id: string;
  title: string;
  description: string;
  approach: string;
  metrics: Array<{ label: string; value: string }>;
  technologies: string[];
  sourceUrl?: string;
  liveUrl?: string;
};

export const profile = {
  firstName: "David",
  surname: "Danielian",
  role: "Machine Learning / Data Science",
  summary:
    "Projects in retrieval, NLP, tabular machine learning and deployable ML systems.",
  github: "https://github.com/Davidkaaa33",
  linkedin: "",
  resume: "/David_Danielian_CV.pdf",
  email: "d.danielian@innopolis.university",
  telegram: "https://t.me/Dava_Djan",
  education:
    "Innopolis University, BSc in Data Analysis and Artificial Intelligence, 2025–2028",
  location: "Innopolis, Russia",
  currentStatus:
    "Second-year BSc student, GPA 4.9/5.0, full-tuition scholarship, programme taught entirely in English"
};

export const profileName = [profile.firstName, profile.surname]
  .filter(Boolean)
  .join(" ");

export const featuredProjects: FeaturedProject[] = [
  {
    id: "avito",
    title: "Avito Data Science Bootcamp 2026",
    description:
      "Hybrid retrieval pipeline for service search with a confirmed Recall@50 of 0.831562.",
    approach:
      "BGE-M3, BM25, geography, microcategories, query history and weighted RRF, evaluated with query-disjoint validation and separate tuning and confirmation splits.",
    metrics: [{ label: "Recall@50", value: "0.831562" }],
    technologies: ["BGE-M3", "BM25", "RRF", "Retrieval", "NLP"],
    sourceUrl: "https://github.com/Davidkaaa33/avito-ds-bootcamp-2026-solution"
  },
  {
    id: "postcode",
    title: "PostCode Challenge 2026 (PochtaTech)",
    description:
      "Team-built ML system for Service Desk categorization and routing. Finished 11th.",
    approach:
      "MiniLM, TF-IDF and metadata features, LinearSVC, semantic retrieval and confidence-based review, with similar-ticket search, SLA analysis, Top-3 predictions and difficult-case re-checking through Qwen3-Embedding-4B + LoRA. Served with FastAPI and React.",
    metrics: [{ label: "Place", value: "11th" }],
    technologies: [
      "MiniLM",
      "TF-IDF",
      "LinearSVC",
      "Semantic Retrieval",
      "Qwen3-Embedding-4B",
      "LoRA",
      "FastAPI",
      "React"
    ]
  },
  {
    id: "systems-lab",
    title: "ML Systems Lab",
    description:
      "Five ML systems combined into one portfolio application: Fraud Detection, Credit Repayment, SMS Spam, T9 Correction and a local RAG system.",
    approach:
      "Serving through FastAPI, React, Docker and CI while keeping the individual systems and their measured results visible.",
    metrics: [
      { label: "Fraud ROC-AUC", value: "0.8713" },
      { label: "T9 Top-1", value: "97.75%" },
      { label: "RAG Hit@1", value: "81.82%" }
    ],
    technologies: ["FastAPI", "React", "Docker", "CI"],
    sourceUrl: "https://github.com/Davidkaaa33/ML-projects",
    liveUrl: "#lab"
  },
  {
    id: "store-order",
    title: "Store Order Management System",
    description:
      "University team project delivered to MVP v3 with responsibility for both technical work and team coordination.",
    approach:
      "Led backlog and sprint planning, task distribution, code review, CI and customer feedback, while contributing to backend, frontend, API work and quality documentation.",
    metrics: [
      { label: "Role", value: "Team Lead" },
      { label: "Release", value: "MVP v3" }
    ],
    technologies: ["Backend", "Frontend", "API", "CI", "Code Review"]
  }
];

export const capabilities = [
  {
    title: "Programming",
    items: ["Python", "SQL", "C++"]
  },
  {
    title: "ML / Data",
    items: ["NumPy", "pandas", "scikit-learn", "CatBoost", "PyTorch"]
  },
  {
    title: "NLP / Retrieval",
    items: [
      "Transformers",
      "SentenceTransformers",
      "BGE-M3",
      "BM25",
      "MiniLM",
      "RRF"
    ]
  },
  {
    title: "Engineering",
    items: ["FastAPI", "Docker", "PostgreSQL", "Git", "GitHub Actions"]
  },
  {
    title: "Methods",
    items: [
      "cross-validation",
      "feature engineering",
      "imbalanced learning",
      "threshold tuning",
      "error analysis"
    ]
  }
] as const;

export const additionalLearning = [
  "DeepLearning.AI: Machine Learning Specialization; Mathematics for Machine Learning and Data Science; Machine Learning in Production",
  "Caltech / ods.ai: Machine Learning; ML System Design Course"
] as const;

export const additionalPractice = [
  "LeetCode: independent problem solving, alternative solutions, optimization and time/space complexity analysis",
  "Deep-ML: ML fundamentals practice with algorithm analysis, computational complexity and trade-offs"
] as const;
