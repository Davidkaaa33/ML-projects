import { useEffect, useMemo, useState } from "react";

import { api } from "./api";
import type { ModelInfo, Overview, RAGEvaluation } from "./types";

const GITHUB = "https://github.com/Davidkaaa33/ML-projects";
const tabs = ["spam", "typo", "fraud", "credit", "rag"] as const;
type DemoTab = (typeof tabs)[number];

function formatPercent(value: number) {
  return `${(value * 100).toFixed(1)}%`;
}

function ModelCard({ model, onOpen }: { model: ModelInfo; onOpen: () => void }) {
  return (
    <article className="model-card">
      <div className="card-topline">
        <span className="status-dot" data-live={model.live} />
        <span>{model.task}</span>
        <span className="scope">{model.data_scope}</span>
      </div>

      <h3>{model.name}</h3>
      <p>{model.description}</p>

      <div className="metric-row">
        <div>
          <span className="metric-label">{model.headline_metric}</span>
          <strong>{model.headline_value}</strong>
        </div>
        <span className="secondary-metric">{model.secondary_metric}</span>
      </div>

      <div className="tag-row">
        {model.technology.map((item) => (
          <span key={item}>{item}</span>
        ))}
      </div>

      <div className="card-actions">
        <button className="text-button" onClick={onOpen}>
          Open demo
        </button>
        <a href={`${GITHUB}/tree/main/${model.repo_path}`} target="_blank" rel="noreferrer">
          Source
        </a>
      </div>
    </article>
  );
}

function OutputBlock({ children }: { children: React.ReactNode }) {
  return <div className="output-block">{children}</div>;
}

function SpamDemo() {
  const [text, setText] = useState("Congratulations! You've won a free prize. Call now to claim.");
  const [result, setResult] = useState<{ label: string; spam_probability: number; confidence: number } | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function run() {
    setBusy(true);
    setError("");
    try {
      setResult(
        await api("/api/spam/predict", {
          method: "POST",
          body: JSON.stringify({ text })
        })
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="demo-grid">
      <div>
        <label className="field-label" htmlFor="spam-input">SMS text</label>
        <textarea
          id="spam-input"
          value={text}
          maxLength={5000}
          onChange={(event) => setText(event.target.value)}
        />
        <div className="example-row">
          <button onClick={() => setText("Call me when you arrive, I'll meet you downstairs.")}>Normal example</button>
          <button onClick={() => setText("URGENT! You have won a £500 reward. Reply WIN now.")}>Spam example</button>
        </div>
        <button className="primary-button" onClick={run} disabled={busy || !text.trim()}>
          {busy ? "Running…" : "Classify message"}
        </button>
      </div>

      <OutputBlock>
        {result ? (
          <>
            <span className="result-kicker">Prediction</span>
            <div className="result-title">{result.label.toUpperCase()}</div>
            <div className="score-line">
              <span>Spam probability</span>
              <strong>{formatPercent(result.spam_probability)}</strong>
            </div>
            <div className="meter"><span style={{ width: formatPercent(result.spam_probability) }} /></div>
            <p className="quiet">TF-IDF + Multinomial Naive Bayes. Exact-message duplicates are removed before the train/test split.</p>
          </>
        ) : (
          <p className="placeholder">Run the classifier to inspect its probability and decision.</p>
        )}
        {error && <p className="error-text">{error}</p>}
      </OutputBlock>
    </div>
  );
}

function TypoDemo() {
  const [text, setText] = useState("I am lerning pythom with fun");
  const [result, setResult] = useState<{
    corrected: string;
    corrections: Array<{
      input: string;
      replacement: string;
      candidates: Array<{ word: string; score: number }>;
    }>;
  } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    setBusy(true);
    setError("");
    try {
      setResult(
        await api("/api/t9/correct", {
          method: "POST",
          body: JSON.stringify({ text })
        })
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Correction failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="demo-grid">
      <div>
        <label className="field-label" htmlFor="typo-input">Input sentence</label>
        <textarea id="typo-input" value={text} onChange={(event) => setText(event.target.value)} />
        <button className="primary-button" onClick={run} disabled={busy || !text.trim()}>
          {busy ? "Ranking…" : "Correct sentence"}
        </button>
      </div>

      <OutputBlock>
        {result ? (
          <>
            <span className="result-kicker">Corrected</span>
            <div className="result-title sentence">{result.corrected}</div>
            <div className="candidate-list">
              {result.corrections.map((item) => (
                <div className="candidate-item" key={item.input}>
                  <div>
                    <span className="mono">{item.input}</span>
                    <span className="arrow">→</span>
                    <strong>{item.replacement}</strong>
                  </div>
                  <span className="quiet">
                    {item.candidates.map((candidate) => `${candidate.word} · ${candidate.score}`).join("  /  ")}
                  </span>
                </div>
              ))}
            </div>
          </>
        ) : (
          <p className="placeholder">The live demo exposes the same deterministic candidate-ranking code evaluated in the project.</p>
        )}
        {error && <p className="error-text">{error}</p>}
      </OutputBlock>
    </div>
  );
}

type RecordExamples = Record<string, Record<string, unknown>>;

function RecordDemo({
  kind
}: {
  kind: "fraud" | "credit";
}) {
  const [examples, setExamples] = useState<RecordExamples | null>(null);
  const [record, setRecord] = useState<Record<string, unknown> | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setError("");
    api<RecordExamples>(`/api/${kind}/examples`)
      .then((data) => {
        setExamples(data);
        setRecord(Object.values(data)[0] ?? null);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Unable to load demo records."));
  }, [kind]);

  const title = kind === "fraud" ? "Transaction risk" : "Repayment probability";

  async function run() {
    if (!record) return;
    setBusy(true);
    setError("");
    try {
      setResult(
        await api(`/api/${kind}/predict`, {
          method: "POST",
          body: JSON.stringify({ record })
        })
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed.");
    } finally {
      setBusy(false);
    }
  }

  const probability =
    typeof result?.fraud_probability === "number"
      ? result.fraud_probability
      : typeof result?.repayment_probability === "number"
        ? result.repayment_probability
        : null;

  return (
    <div className="demo-grid">
      <div>
        <span className="field-label">Synthetic example record</span>
        <div className="example-row">
          {examples &&
            Object.entries(examples).map(([name, value]) => (
              <button
                key={name}
                className={record === value ? "selected" : ""}
                onClick={() => {
                  setRecord(value);
                  setResult(null);
                }}
              >
                {name.replaceAll("_", " ")}
              </button>
            ))}
        </div>

        <div className="record-grid">
          {record &&
            Object.entries(record).slice(0, 12).map(([key, value]) => (
              <div key={key}>
                <span>{key.replaceAll("_", " ")}</span>
                <strong>{String(value)}</strong>
              </div>
            ))}
        </div>

        <button className="primary-button" onClick={run} disabled={busy || !record}>
          {busy ? "Fitting demo model…" : `Analyze ${kind === "fraud" ? "transaction" : "customer"}`}
        </button>
        <p className="quiet compact">
          First run lazily fits the selected Random Forest configuration on the full synthetic dataset for demo inference.
        </p>
      </div>

      <OutputBlock>
        {result && probability !== null ? (
          <>
            <span className="result-kicker">{title}</span>
            <div className="result-title">{formatPercent(probability)}</div>
            <div className="score-line">
              <span>Decision</span>
              <strong>{String(result.risk_band).toUpperCase()}</strong>
            </div>
            <div className="meter"><span style={{ width: formatPercent(probability) }} /></div>
            <p className="quiet">{String(result.model_note)}</p>
          </>
        ) : (
          <p className="placeholder">Choose an example and run the real sklearn pipeline. Benchmark metrics remain isolated from demo inference.</p>
        )}
        {error && <p className="error-text">{error}</p>}
      </OutputBlock>
    </div>
  );
}

function RAGDemo() {
  const [evaluation, setEvaluation] = useState<RAGEvaluation | null>(null);
  const [status, setStatus] = useState<{ available: boolean; configured: boolean; detail?: string } | null>(null);
  const [question, setQuestion] = useState("How many days per week can I work remotely?");
  const [answer, setAnswer] = useState<Record<string, unknown> | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    void Promise.all([
      api<RAGEvaluation>("/api/rag/evaluation").then(setEvaluation),
      api<{ available: boolean; configured: boolean; detail?: string }>("/api/rag/status").then(setStatus)
    ]);
  }, []);

  async function run() {
    setBusy(true);
    try {
      setAnswer(
        await api("/api/rag/ask", {
          method: "POST",
          body: JSON.stringify({ question, top_k: 3 })
        })
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="demo-grid">
      <div>
        <div className="rag-status">
          <span className="status-dot" data-live={Boolean(status?.available)} />
          <span>{status?.available ? "Local generation connected" : "Evaluation mode"}</span>
        </div>

        <label className="field-label" htmlFor="rag-question">Question</label>
        <textarea id="rag-question" value={question} onChange={(event) => setQuestion(event.target.value)} />
        <button className="primary-button" onClick={run} disabled={!status?.available || busy || !question.trim()}>
          {status?.available ? (busy ? "Retrieving…" : "Ask knowledge base") : "Start optional RAG service to query"}
        </button>
        {!status?.available && (
          <p className="quiet compact">
            Retrieval evaluation is always available. Live generation is intentionally separated and only enabled when the local Qwen/Ollama service is running.
          </p>
        )}
      </div>

      <OutputBlock>
        {answer ? (
          <>
            <span className="result-kicker">Answer</span>
            <div className="answer-text">{String(answer.answer)}</div>
          </>
        ) : evaluation ? (
          <>
            <span className="result-kicker">Committed evaluation</span>
            <div className="evaluation-grid">
              <div><span>Hit@1</span><strong>{formatPercent(evaluation.retrieval.hit_at_1)}</strong></div>
              <div><span>Hit@3</span><strong>{formatPercent(evaluation.retrieval.hit_at_3)}</strong></div>
              <div><span>MRR@3</span><strong>{evaluation.retrieval.mrr_at_3.toFixed(4)}</strong></div>
              <div><span>Abstention threshold</span><strong>{evaluation.abstention.threshold.toFixed(5)}</strong></div>
            </div>
            <p className="quiet">
              Threshold balanced accuracy: {formatPercent(evaluation.abstention.balanced_accuracy)}. It remains opt-in because the calibration set is intentionally small.
            </p>
          </>
        ) : (
          <p className="placeholder">Loading evaluation artifact…</p>
        )}
      </OutputBlock>
    </div>
  );
}

function LiveLab({
  active,
  setActive
}: {
  active: DemoTab;
  setActive: (tab: DemoTab) => void;
}) {
  return (
    <section className="section" id="lab">
      <div className="section-heading">
        <span className="eyebrow">Interactive inference</span>
        <h2>Live lab</h2>
        <p>One interface over independently evaluated systems. Demo behavior is separated from benchmark claims.</p>
      </div>

      <div className="lab-shell">
        <div className="tab-bar" role="tablist">
          {tabs.map((tab) => (
            <button key={tab} className={active === tab ? "active" : ""} onClick={() => setActive(tab)}>
              {tab === "typo" ? "T9" : tab.toUpperCase()}
            </button>
          ))}
        </div>

        <div className="lab-body">
          {active === "spam" && <SpamDemo />}
          {active === "typo" && <TypoDemo />}
          {active === "fraud" && <RecordDemo kind="fraud" />}
          {active === "credit" && <RecordDemo kind="credit" />}
          {active === "rag" && <RAGDemo />}
        </div>
      </div>
    </section>
  );
}

function App() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [active, setActive] = useState<DemoTab>("spam");

  useEffect(() => {
    api<Overview>("/api/overview").then(setOverview).catch(() => setOverview(null));
  }, []);

  const modelMap = useMemo(
    () => new Map(overview?.models.map((model) => [model.id, model]) ?? []),
    [overview]
  );

  function openModel(id: ModelInfo["id"]) {
    if (id === "typo") setActive("typo");
    else setActive(id);
    document.getElementById("lab")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <div className="site-shell">
      <header className="topbar">
        <a className="brand" href="#top">
          <span className="brand-mark">ML</span>
          <span>Systems Lab</span>
        </a>
        <nav>
          <a href="#systems">Systems</a>
          <a href="#lab">Live lab</a>
          <a href="#architecture">Architecture</a>
          <a href={GITHUB} target="_blank" rel="noreferrer">GitHub ↗</a>
        </nav>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <span className="eyebrow">ML engineering portfolio</span>
            <h1>Models that leave the notebook.</h1>
            <p>
              Five independently evaluated ML systems exposed through a unified API and one restrained interface —
              with tests, Docker, CI and reproducible metrics.
            </p>
            <div className="hero-actions">
              <a className="primary-link" href="#lab">Open live lab</a>
              <a className="secondary-link" href={GITHUB} target="_blank" rel="noreferrer">Inspect repository</a>
            </div>
          </div>

          <div className="proof-panel">
            <div><strong>{overview?.systems ?? 5}</strong><span>ML systems</span></div>
            <div><strong>2</strong><span>API services</span></div>
            <div><strong>CI</strong><span>quality gates</span></div>
            <div><strong>JSON</strong><span>metric artifacts</span></div>
          </div>
        </section>

        <section className="section" id="systems">
          <div className="section-heading">
            <span className="eyebrow">Selected systems</span>
            <h2>Different tasks, one engineering standard.</h2>
            <p>Metrics below come from committed evaluation artifacts, not from the interactive demo session.</p>
          </div>

          <div className="model-grid">
            {(overview?.models ?? []).map((model) => (
              <ModelCard key={model.id} model={model} onOpen={() => openModel(model.id)} />
            ))}
            {!overview && (
              <div className="api-offline">
                <strong>API not connected.</strong>
                <span>Run the full stack with <code>docker compose up --build</code>.</span>
              </div>
            )}
          </div>
        </section>

        <LiveLab active={active} setActive={setActive} />

        <section className="section" id="architecture">
          <div className="section-heading">
            <span className="eyebrow">System design</span>
            <h2>One product surface, explicit model boundaries.</h2>
            <p>The web app never imports model code. A typed FastAPI layer owns inference and delegates the heavy RAG runtime to an optional service.</p>
          </div>

          <div className="architecture">
            <div className="arch-node featured">
              <span>Interface</span>
              <strong>React / Vite</strong>
              <small>single recruiter-facing product surface</small>
            </div>
            <div className="arch-arrow">↓</div>
            <div className="arch-node featured">
              <span>Gateway</span>
              <strong>Unified FastAPI</strong>
              <small>typed contracts · model registry · inference adapters</small>
            </div>
            <div className="arch-arrow">↓</div>
            <div className="arch-grid">
              <div className="arch-node"><strong>Fraud</strong><small>sklearn pipeline</small></div>
              <div className="arch-node"><strong>Credit</strong><small>sklearn pipeline</small></div>
              <div className="arch-node"><strong>Spam</strong><small>joblib inference</small></div>
              <div className="arch-node"><strong>T9</strong><small>candidate ranking</small></div>
              <div className="arch-node"><strong>RAG</strong><small>optional FAISS + Qwen service</small></div>
            </div>
          </div>

          <div className="engineering-grid">
            <div><span>Evaluation</span><strong>Held-out metrics + machine-readable snapshots</strong></div>
            <div><span>Quality</span><strong>Ruff · pytest · compile checks · vulnerability audit</strong></div>
            <div><span>Serving</span><strong>FastAPI · Docker · health checks · smoke tests</strong></div>
            <div><span>RAG controls</span><strong>Pinned embeddings · abstention · metric drift gate</strong></div>
          </div>
        </section>
      </main>

      <footer>
        <span>ML Systems Lab</span>
        <span>Python 3.12 · React · FastAPI · Docker</span>
        <a href={GITHUB} target="_blank" rel="noreferrer">Source ↗</a>
      </footer>
    </div>
  );
}

export default App;
