import { useEffect, useMemo, useState } from "react";

import { api, apiTrace, type ApiTrace } from "./api";
import type {
  CalibrationRecord,
  ModelId,
  ModelInfo,
  Overview,
  RAGEvaluation
} from "./types";

const GITHUB = "https://github.com/Davidkaaa33/ML-projects";
const serviceOrder: ModelId[] = ["rag", "fraud", "credit", "typo", "spam"];

const endpointByModel: Record<ModelId, string> = {
  spam: "/api/spam/predict",
  typo: "/api/t9/correct",
  fraud: "/api/fraud/predict",
  credit: "/api/credit/predict",
  rag: "/api/rag/evaluation"
};

function formatPercent(value: number, digits = 1) {
  return `${(value * 100).toFixed(digits)}%`;
}

function formatScore(value: number) {
  return value.toFixed(3);
}

function clamp(value: number, min = 0, max = 1) {
  return Math.min(max, Math.max(min, value));
}

function ProbabilityRail({
  value,
  marker,
  label
}: {
  value: number;
  marker?: number;
  label: string;
}) {
  const safe = clamp(value);
  return (
    <div className="probability-block">
      <div className="probability-labels">
        <span>{label}</span>
        <strong>{formatPercent(safe)}</strong>
      </div>
      <div className="probability-rail" aria-label={label}>
        <span className="probability-fill" style={{ width: formatPercent(safe, 2) }} />
        {typeof marker === "number" && (
          <span
            className="threshold-marker"
            style={{ left: formatPercent(clamp(marker), 2) }}
            title={`Decision threshold ${marker.toFixed(3)}`}
          />
        )}
      </div>
    </div>
  );
}

function RunButton({
  busy,
  disabled,
  onClick,
  children
}: {
  busy: boolean;
  disabled?: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      className="run-button"
      onClick={onClick}
      disabled={disabled || busy}
      data-busy={busy}
    >
      <span className="run-icon">{busy ? "···" : "▶"}</span>
      <span>{busy ? "Running model…" : children}</span>
    </button>
  );
}

function History({
  items,
  onSelect
}: {
  items: Array<{ id: number; title: string; detail: string; value: string }>;
  onSelect?: (id: number) => void;
}) {
  if (!items.length) return null;

  return (
    <div className="history-block">
      <div className="subsection-title">Recent runs</div>
      <div className="history-list">
        {items.slice(0, 5).map((item) => (
          <button
            key={item.id}
            className="history-row"
            onClick={() => onSelect?.(item.id)}
            disabled={!onSelect}
          >
            <span className="history-title">{item.title}</span>
            <span className="history-detail">{item.detail}</span>
            <strong>{item.value}</strong>
          </button>
        ))}
      </div>
    </div>
  );
}

function RequestInspector<T>({ trace }: { trace: ApiTrace<T> | null }) {
  if (!trace) return null;

  return (
    <details className="request-inspector">
      <summary>
        <span>Inspect API request</span>
        <span className="inspector-meta">
          {trace.method} · {Math.round(trace.durationMs)} ms
        </span>
      </summary>
      <div className="inspector-content">
        <div>
          <span className="result-caption">Endpoint</span>
          <code>{trace.endpoint}</code>
        </div>
        <div>
          <span className="result-caption">Request</span>
          <pre>{JSON.stringify(trace.request, null, 2)}</pre>
        </div>
        <div>
          <span className="result-caption">Response</span>
          <pre>{JSON.stringify(trace.response, null, 2)}</pre>
        </div>
      </div>
    </details>
  );
}

function SpamDemo() {
  const presets = [
    {
      name: "Normal",
      text: "Call me when you arrive, I'll meet you downstairs."
    },
    {
      name: "Prize spam",
      text: "URGENT! You have won a £500 reward. Reply WIN now to claim your prize."
    },
    {
      name: "Promo",
      text: "Free entry in our weekly prize draw. Text YES now for your chance to win."
    },
    {
      name: "Personal",
      text: "Can you send me the notes from today's meeting when you get a chance?"
    }
  ];

  type SpamResult = {
    label: string;
    spam_probability: number;
    confidence: number;
  };

  type SpamHistory = {
    id: number;
    text: string;
    result: SpamResult;
  };

  const [text, setText] = useState(presets[1].text);
  const [result, setResult] = useState<SpamResult | null>(null);
  const [trace, setTrace] = useState<ApiTrace<SpamResult> | null>(null);
  const [threshold, setThreshold] = useState(0.5);
  const [history, setHistory] = useState<SpamHistory[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    if (!text.trim()) return;
    setBusy(true);
    setError("");
    try {
      const traced = await apiTrace<SpamResult>("/api/spam/predict", {
        method: "POST",
        body: JSON.stringify({ text })
      });
      const next = traced.data;
      setTrace(traced);
      setResult(next);
      setHistory((items) => [
        { id: Date.now(), text, result: next },
        ...items
      ].slice(0, 5));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="playground-layout">
      <section className="input-pane">
        <div className="toolbar">
          <div className="preset-group">
            {presets.map((preset) => (
              <button
                key={preset.name}
                className="control-button"
                onClick={() => {
                  setText(preset.text);
                  setResult(null);
                  setTrace(null);
                }}
              >
                {preset.name}
              </button>
            ))}
          </div>
          <button
            className="control-button subtle"
            onClick={() => {
              setText("");
              setResult(null);
              setTrace(null);
            }}
          >
            Clear
          </button>
        </div>

        <label className="field-label" htmlFor="spam-input">
          SMS message
        </label>
        <textarea
          id="spam-input"
          value={text}
          maxLength={5000}
          spellCheck={false}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
              event.preventDefault();
              void run();
            }
          }}
        />
        <div className="input-meta">
          <span>{text.length} / 5000 chars</span>
          <span>⌘ / Ctrl + Enter to run</span>
        </div>

        <RunButton busy={busy} disabled={!text.trim()} onClick={() => void run()}>
          Classify message
        </RunButton>
        {error && <div className="error-banner">{error}</div>}

        <History
          items={history.map((item) => ({
            id: item.id,
            title: item.text.slice(0, 48),
            detail: item.result.label.toUpperCase(),
            value: formatPercent(item.result.spam_probability)
          }))}
          onSelect={(id) => {
            const item = history.find((entry) => entry.id === id);
            if (item) {
              setText(item.text);
              setResult(item.result);
              setTrace(null);
            }
          }}
        />
      </section>

      <section className="result-pane">
        <div className="panel-heading">
          <span>Model output</span>
          <span className="mono-label">TF-IDF · Multinomial NB</span>
        </div>

        {result ? (
          <div className="result-content" key={`${result.label}-${result.spam_probability}`}>
            <div className="decision-row">
              <div>
                <span className="result-caption">Decision at current threshold</span>
                <strong className="decision-value">
                  {result.spam_probability >= threshold ? "SPAM" : "HAM"}
                </strong>
              </div>
              <span className="decision-badge neutral">
                p(spam) {formatPercent(result.spam_probability)}
              </span>
            </div>

            <ProbabilityRail
              value={result.spam_probability}
              marker={threshold}
              label="Spam probability"
            />

            <div className="threshold-editor">
              <div>
                <span>Decision threshold</span>
                <strong>{threshold.toFixed(2)}</strong>
              </div>
              <input
                type="range"
                min="0.05"
                max="0.95"
                step="0.05"
                value={threshold}
                onChange={(event) => setThreshold(Number(event.target.value))}
              />
              <button className="control-button subtle" onClick={() => setThreshold(0.5)}>
                Reset 0.50
              </button>
            </div>

            <div className="explain-list">
              <div>
                <span>Input handling</span>
                <strong>Exact-message deduplication before split</strong>
              </div>
              <div>
                <span>Benchmark</span>
                <strong>Precision 1.0000 · F1 0.7642</strong>
              </div>
            </div>
            <RequestInspector trace={trace} />
          </div>
        ) : (
          <div className="empty-state">
            <strong>Run a message through the classifier.</strong>
            <span>The output will show the actual model probability, not a mocked UI state.</span>
          </div>
        )}
      </section>
    </div>
  );
}

function TypoDemo() {
  const presets = [
    "I am lerning pythom with fun",
    "machne lerning is usefull",
    "I realy enjoy programing",
    "deep lerning modls are powerfull"
  ];

  type TypoResult = {
    input: string;
    corrected: string;
    corrections: Array<{
      input: string;
      replacement: string;
      candidates: Array<{ word: string; score: number }>;
    }>;
  };

  type TypoHistory = {
    id: number;
    input: string;
    result: TypoResult;
  };

  const [text, setText] = useState(presets[0]);
  const [result, setResult] = useState<TypoResult | null>(null);
  const [trace, setTrace] = useState<ApiTrace<TypoResult> | null>(null);
  const [history, setHistory] = useState<TypoHistory[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    if (!text.trim()) return;
    setBusy(true);
    setError("");
    try {
      const traced = await apiTrace<TypoResult>("/api/t9/correct", {
        method: "POST",
        body: JSON.stringify({ text })
      });
      const next = traced.data;
      setTrace(traced);
      setResult(next);
      setHistory((items) => [
        { id: Date.now(), input: text, result: next },
        ...items
      ].slice(0, 5));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Correction failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="playground-layout">
      <section className="input-pane">
        <div className="toolbar">
          <div className="preset-group">
            {presets.map((preset, index) => (
              <button
                key={preset}
                className="control-button"
                onClick={() => {
                  setText(preset);
                  setResult(null);
                  setTrace(null);
                }}
              >
                Example {index + 1}
              </button>
            ))}
          </div>
          <button
            className="control-button subtle"
            onClick={() => {
              setText("");
              setResult(null);
              setTrace(null);
            }}
          >
            Clear
          </button>
        </div>

        <label className="field-label" htmlFor="typo-input">
          Sentence
        </label>
        <textarea
          id="typo-input"
          value={text}
          spellCheck={false}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
              event.preventDefault();
              void run();
            }
          }}
        />

        <RunButton busy={busy} disabled={!text.trim()} onClick={() => void run()}>
          Rank corrections
        </RunButton>
        {error && <div className="error-banner">{error}</div>}

        <History
          items={history.map((item) => ({
            id: item.id,
            title: item.input,
            detail: `${item.result.corrections.length} correction(s)`,
            value: item.result.corrected.slice(0, 34)
          }))}
          onSelect={(id) => {
            const item = history.find((entry) => entry.id === id);
            if (item) {
              setText(item.input);
              setResult(item.result);
              setTrace(null);
            }
          }}
        />
      </section>

      <section className="result-pane">
        <div className="panel-heading">
          <span>Ranked candidates</span>
          <span className="mono-label">Levenshtein · deterministic scoring</span>
        </div>

        {result ? (
          <div className="result-content" key={result.corrected}>
            <div className="corrected-sentence">{result.corrected}</div>

            {result.corrections.length ? (
              <div className="correction-stack">
                {result.corrections.map((item) => {
                  const maxScore = Math.max(
                    ...item.candidates.map((candidate) => candidate.score),
                    0.0001
                  );

                  return (
                    <div className="correction-block" key={item.input}>
                      <div className="correction-title">
                        <span className="mono-word">{item.input}</span>
                        <span>→</span>
                        <strong>{item.replacement}</strong>
                      </div>
                      <div className="candidate-stack">
                        {item.candidates.map((candidate, index) => (
                          <div className="candidate-row" key={candidate.word}>
                            <span className="candidate-rank">{index + 1}</span>
                            <span>{candidate.word}</span>
                            <div className="candidate-bar">
                              <span
                                style={{
                                  width: formatPercent(
                                    clamp(candidate.score / maxScore),
                                    2
                                  )
                                }}
                              />
                            </div>
                            <strong>{candidate.score.toFixed(3)}</strong>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="inline-note">No corrections were required.</div>
            )}
            <RequestInspector trace={trace} />
          </div>
        ) : (
          <div className="empty-state">
            <strong>Try a misspelled sentence.</strong>
            <span>You will see the selected replacement and the real ranked candidate list.</span>
          </div>
        )}
      </section>
    </div>
  );
}

type RecordExamples = Record<string, Record<string, unknown>>;

type RecordPrediction = {
  fraud_probability?: number;
  repayment_probability?: number;
  threshold?: number;
  prediction?: number;
  risk_band?: string;
  model_note?: string;
  benchmark?: Record<string, number>;
};

function RecordDemo({ kind }: { kind: "fraud" | "credit" }) {
  const [examples, setExamples] = useState<RecordExamples | null>(null);
  const [selectedPreset, setSelectedPreset] = useState("");
  const [record, setRecord] = useState<Record<string, unknown> | null>(null);
  const [result, setResult] = useState<RecordPrediction | null>(null);
  const [trace, setTrace] = useState<ApiTrace<RecordPrediction> | null>(null);
  const [history, setHistory] = useState<
    Array<{
      id: number;
      preset: string;
      probability: number;
      record: Record<string, unknown>;
      result: RecordPrediction;
    }>
  >([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setError("");
    api<RecordExamples>(`/api/${kind}/examples`)
      .then((data) => {
        setExamples(data);
        const first = Object.entries(data)[0];
        if (first) {
          setSelectedPreset(first[0]);
          setRecord({ ...first[1] });
        }
      })
      .catch((err) => {
        setError(
          err instanceof Error ? err.message : "Unable to load example records."
        );
      });
  }, [kind]);

  function choosePreset(name: string, value: Record<string, unknown>) {
    setSelectedPreset(name);
    setRecord({ ...value });
    setResult(null);
    setTrace(null);
  }

  function resetPreset() {
    if (!examples || !selectedPreset || !examples[selectedPreset]) return;
    setRecord({ ...examples[selectedPreset] });
    setResult(null);
    setTrace(null);
  }

  function updateField(key: string, raw: string) {
    setRecord((current) => {
      if (!current) return current;
      const previous = current[key];
      let value: unknown = raw;
      if (typeof previous === "number") {
        const parsed = Number(raw);
        value = Number.isNaN(parsed) ? previous : parsed;
      }
      return { ...current, [key]: value };
    });
  }

  async function run() {
    if (!record) return;
    setBusy(true);
    setError("");
    try {
      const traced = await apiTrace<RecordPrediction>(`/api/${kind}/predict`, {
        method: "POST",
        body: JSON.stringify({ record })
      });
      const next = traced.data;
      setTrace(traced);
      setResult(next);

      const probability =
        typeof next.fraud_probability === "number"
          ? next.fraud_probability
          : next.repayment_probability ?? 0;

      setHistory((items) => [
        {
          id: Date.now(),
          preset: selectedPreset || "edited",
          probability,
          record: { ...record },
          result: next
        },
        ...items
      ].slice(0, 5));
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

  const marker =
    kind === "fraud"
      ? result?.threshold
      : 0.5;

  return (
    <div className="playground-layout record-playground">
      <section className="input-pane">
        <div className="toolbar">
          <div className="preset-group">
            {examples &&
              Object.entries(examples).map(([name, value]) => (
                <button
                  key={name}
                  className={`control-button ${selectedPreset === name ? "selected" : ""}`}
                  onClick={() => choosePreset(name, value)}
                >
                  {name.replaceAll("_", " ")}
                </button>
              ))}
          </div>
          <button className="control-button subtle" onClick={resetPreset}>
            Reset values
          </button>
        </div>

        <div className="subsection-title">Editable model input</div>
        <div className="field-editor">
          {record &&
            Object.entries(record).map(([key, value]) => (
              <label className="record-field" key={key}>
                <span>{key.replaceAll("_", " ")}</span>
                <input
                  value={String(value ?? "")}
                  type={typeof value === "number" ? "number" : "text"}
                  step={typeof value === "number" ? "any" : undefined}
                  onChange={(event) => updateField(key, event.target.value)}
                />
              </label>
            ))}
        </div>

        <RunButton busy={busy} disabled={!record} onClick={() => void run()}>
          {kind === "fraud" ? "Score transaction" : "Score customer"}
        </RunButton>
        <div className="inline-note">
          The first request may take a moment while the selected Random Forest configuration is fitted for interactive inference.
        </div>
        {error && <div className="error-banner">{error}</div>}

        <History
          items={history.map((item) => ({
            id: item.id,
            title: item.preset.replaceAll("_", " "),
            detail: String(item.result.risk_band ?? "scored").toUpperCase(),
            value: formatPercent(item.probability)
          }))}
          onSelect={(id) => {
            const item = history.find((entry) => entry.id === id);
            if (item) {
              setRecord({ ...item.record });
              setResult(item.result);
              setTrace(null);
            }
          }}
        />
      </section>

      <section className="result-pane">
        <div className="panel-heading">
          <span>{kind === "fraud" ? "Transaction risk" : "Repayment score"}</span>
          <span className="mono-label">Random Forest · sklearn Pipeline</span>
        </div>

        {result && probability !== null ? (
          <div className="result-content" key={probability}>
            <div className="decision-row">
              <div>
                <span className="result-caption">Probability</span>
                <strong className="decision-value">{formatPercent(probability)}</strong>
              </div>
              <span className="decision-badge neutral">
                {String(result.risk_band ?? "scored").toUpperCase()}
              </span>
            </div>

            <ProbabilityRail
              value={probability}
              marker={marker}
              label={kind === "fraud" ? "Fraud probability" : "Repayment probability"}
            />

            {typeof marker === "number" && (
              <div className="threshold-readout">
                <span>Decision threshold</span>
                <strong>{marker.toFixed(3)}</strong>
              </div>
            )}

            {result.benchmark && (
              <div className="benchmark-table">
                {Object.entries(result.benchmark).map(([metric, value]) => (
                  <div key={metric}>
                    <span>{metric.replaceAll("_", " ")}</span>
                    <strong>{Number(value).toFixed(4)}</strong>
                  </div>
                ))}
              </div>
            )}

            <div className="inline-note">
              Benchmark metrics come from the held-out test split; this playground result does not overwrite them.
            </div>
            <RequestInspector trace={trace} />
          </div>
        ) : (
          <div className="empty-state">
            <strong>Edit a real example record, then score it.</strong>
            <span>
              Inputs are sent to the same preprocessing + model pipeline used by the project code.
            </span>
          </div>
        )}
      </section>
    </div>
  );
}

function RAGScorePlot({
  records,
  threshold,
  selectedId,
  onSelect
}: {
  records: CalibrationRecord[];
  threshold: number;
  selectedId: number | null;
  onSelect: (id: number) => void;
}) {
  return (
    <div className="score-plot">
      <div
        className="plot-threshold"
        style={{ left: formatPercent(threshold, 2) }}
      >
        <span>{threshold.toFixed(3)}</span>
      </div>
      <div className="plot-lane">
        <span className="plot-lane-label">Answerable</span>
        <div className="plot-track">
          {records
            .filter((record) => record.answerable)
            .map((record) => (
              <button
                key={record.id}
                className={`plot-dot answerable ${selectedId === record.id ? "selected" : ""}`}
                style={{ left: formatPercent(record.top_score, 2) }}
                title={`${record.question} — ${record.top_score.toFixed(3)}`}
                onClick={() => onSelect(record.id)}
              />
            ))}
        </div>
      </div>
      <div className="plot-lane">
        <span className="plot-lane-label">Unsupported</span>
        <div className="plot-track">
          {records
            .filter((record) => !record.answerable)
            .map((record) => (
              <button
                key={record.id}
                className={`plot-dot unsupported ${selectedId === record.id ? "selected" : ""}`}
                style={{ left: formatPercent(record.top_score, 2) }}
                title={`${record.question} — ${record.top_score.toFixed(3)}`}
                onClick={() => onSelect(record.id)}
              />
            ))}
        </div>
      </div>
      <div className="plot-axis">
        <span>0.0</span>
        <span>0.25</span>
        <span>0.5</span>
        <span>0.75</span>
        <span>1.0</span>
      </div>
    </div>
  );
}

function RAGDemo() {
  const [evaluation, setEvaluation] = useState<RAGEvaluation | null>(null);
  const [status, setStatus] = useState<{
    available: boolean;
    configured: boolean;
    detail?: string;
  } | null>(null);
  const [threshold, setThreshold] = useState(0.6);
  const [filter, setFilter] = useState<"all" | "answerable" | "unsupported">("all");
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [question, setQuestion] = useState(
    "How many days per week can I work remotely?"
  );
  const [answer, setAnswer] = useState<Record<string, unknown> | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void Promise.all([
      api<RAGEvaluation>("/api/rag/evaluation").then((data) => {
        setEvaluation(data);
        setThreshold(data.abstention.threshold);
        setSelectedId(data.calibration_records[0]?.id ?? null);
      }),
      api<{ available: boolean; configured: boolean; detail?: string }>(
        "/api/rag/status"
      ).then(setStatus)
    ]).catch((err) => {
      setError(err instanceof Error ? err.message : "Unable to load RAG evaluation.");
    });
  }, []);

  const simulated = useMemo(() => {
    if (!evaluation) return null;

    const answerable = evaluation.calibration_records.filter(
      (record) => record.answerable
    );
    const unsupported = evaluation.calibration_records.filter(
      (record) => !record.answerable
    );

    const answerableRecall =
      answerable.filter((record) => record.top_score >= threshold).length /
      Math.max(answerable.length, 1);

    const unsupportedRecall =
      unsupported.filter((record) => record.top_score < threshold).length /
      Math.max(unsupported.length, 1);

    return {
      answerableRecall,
      unsupportedRecall,
      balancedAccuracy: (answerableRecall + unsupportedRecall) / 2
    };
  }, [evaluation, threshold]);

  const visibleRecords = useMemo(() => {
    if (!evaluation) return [];
    return evaluation.calibration_records
      .filter((record) => {
        if (filter === "answerable") return record.answerable;
        if (filter === "unsupported") return !record.answerable;
        return true;
      })
      .sort((left, right) => right.top_score - left.top_score);
  }, [evaluation, filter]);

  const selectedRecord =
    evaluation?.calibration_records.find((record) => record.id === selectedId) ??
    null;

  async function runLive() {
    if (!status?.available || !question.trim()) return;
    setBusy(true);
    setError("");
    try {
      setAnswer(
        await api("/api/rag/ask", {
          method: "POST",
          body: JSON.stringify({ question, top_k: 3 })
        })
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "RAG request failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="rag-workbench">
      <section className="rag-control-pane">
        <div className="panel-heading">
          <span>Retrieval threshold simulator</span>
          <span className="mono-label">
            {evaluation ? `${evaluation.calibration_records.length} labeled queries` : "loading"}
          </span>
        </div>

        {evaluation && simulated ? (
          <>
            <div className="threshold-controls">
              <div className="threshold-header">
                <div>
                  <span className="result-caption">Current threshold</span>
                  <strong>{threshold.toFixed(3)}</strong>
                </div>
                <div className="button-row">
                  <button
                    className="control-button"
                    onClick={() =>
                      setThreshold(
                        clamp(evaluation.abstention.threshold - 0.05)
                      )
                    }
                  >
                    More permissive
                  </button>
                  <button
                    className="control-button selected"
                    onClick={() => setThreshold(evaluation.abstention.threshold)}
                  >
                    Calibrated
                  </button>
                  <button
                    className="control-button"
                    onClick={() =>
                      setThreshold(
                        clamp(evaluation.abstention.threshold + 0.05)
                      )
                    }
                  >
                    Stricter
                  </button>
                </div>
              </div>

              <input
                className="threshold-slider"
                type="range"
                min="0"
                max="1"
                step="0.005"
                value={threshold}
                onChange={(event) => setThreshold(Number(event.target.value))}
              />
            </div>

            <div className="sim-metrics">
              <div>
                <span>Balanced accuracy</span>
                <strong>{formatPercent(simulated.balancedAccuracy)}</strong>
              </div>
              <div>
                <span>Answerable recall</span>
                <strong>{formatPercent(simulated.answerableRecall)}</strong>
              </div>
              <div>
                <span>Unsupported recall</span>
                <strong>{formatPercent(simulated.unsupportedRecall)}</strong>
              </div>
            </div>

            <RAGScorePlot
              records={evaluation.calibration_records}
              threshold={threshold}
              selectedId={selectedId}
              onSelect={setSelectedId}
            />

            {selectedRecord && (
              <div className="selected-query">
                <span className="result-caption">Selected calibration query</span>
                <strong>{selectedRecord.question}</strong>
                <div className="selected-query-meta">
                  <span>score {selectedRecord.top_score.toFixed(3)}</span>
                  <span>
                    expected {selectedRecord.answerable ? "ANSWERABLE" : "UNSUPPORTED"}
                  </span>
                  <span
                    className={
                      selectedRecord.top_score >= threshold
                        ? "action-answer"
                        : "action-abstain"
                    }
                  >
                    current action{" "}
                    {selectedRecord.top_score >= threshold ? "ANSWER" : "ABSTAIN"}
                  </span>
                </div>
              </div>
            )}

            <div className="filter-row">
              {(["all", "answerable", "unsupported"] as const).map((value) => (
                <button
                  key={value}
                  className={`control-button ${filter === value ? "selected" : ""}`}
                  onClick={() => setFilter(value)}
                >
                  {value}
                </button>
              ))}
            </div>

            <div className="query-table">
              {visibleRecords.map((record) => (
                <button
                  key={record.id}
                  className={`query-row ${selectedId === record.id ? "selected" : ""}`}
                  onClick={() => {
                    setSelectedId(record.id);
                    setQuestion(record.question);
                  }}
                >
                  <span className="query-kind">
                    {record.answerable ? "answerable" : "unsupported"}
                  </span>
                  <span className="query-text">{record.question}</span>
                  <strong>{formatScore(record.top_score)}</strong>
                  <span
                    className={
                      record.top_score >= threshold
                        ? "action-answer"
                        : "action-abstain"
                    }
                  >
                    {record.top_score >= threshold ? "answer" : "abstain"}
                  </span>
                </button>
              ))}
            </div>
          </>
        ) : (
          <div className="empty-state">
            <strong>Loading evaluation snapshot…</strong>
          </div>
        )}
      </section>

      <section className="rag-live-pane">
        <div className="panel-heading">
          <span>Generation</span>
          <span className="mono-label">
            {status?.available ? "local runtime connected" : "public runtime disabled"}
          </span>
        </div>

        <label className="field-label" htmlFor="rag-question">
          Question
        </label>
        <textarea
          id="rag-question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
        />

        <RunButton
          busy={busy}
          disabled={!status?.available || !question.trim()}
          onClick={() => void runLive()}
        >
          Ask knowledge base
        </RunButton>

        {!status?.available && (
          <div className="inline-note">
            Public hosting keeps the heavy Qwen/Ollama runtime disabled. The retrieval and abstention simulator above uses the committed real evaluation scores and stays fully interactive.
          </div>
        )}

        {answer && (
          <div className="live-answer">
            <span className="result-caption">Answer</span>
            <p>{String(answer.answer ?? "")}</p>
          </div>
        )}

        {evaluation && (
          <div className="benchmark-table">
            <div>
              <span>Hit@1</span>
              <strong>{formatPercent(evaluation.retrieval.hit_at_1)}</strong>
            </div>
            <div>
              <span>Hit@3</span>
              <strong>{formatPercent(evaluation.retrieval.hit_at_3)}</strong>
            </div>
            <div>
              <span>MRR@3</span>
              <strong>{evaluation.retrieval.mrr_at_3.toFixed(4)}</strong>
            </div>
            <div>
              <span>Calibrated threshold</span>
              <strong>{evaluation.abstention.threshold.toFixed(5)}</strong>
            </div>
          </div>
        )}

        {error && <div className="error-banner">{error}</div>}
      </section>
    </div>
  );
}

function SystemHeader({
  model,
  copied,
  onCopy
}: {
  model: ModelInfo;
  copied: boolean;
  onCopy: () => void;
}) {
  return (
    <header className="system-header">
      <div className="system-heading">
        <h1>{model.name}</h1>
        <p>{model.description}</p>

        <div className="benchmark-line">
          <span>
            <strong>{model.headline_metric}</strong> {model.headline_value}
          </span>
          <span>{model.secondary_metric}</span>
          <span>{model.data_scope}</span>
        </div>

        <div className="system-meta">{model.technology.join(" · ")}</div>
      </div>

      <nav className="system-actions" aria-label="System links">
        <button className="utility-button" onClick={onCopy}>
          {copied ? "Endpoint copied" : "Copy endpoint"}
        </button>
        <a
          className="utility-button"
          href={`${GITHUB}/tree/main/${model.repo_path}`}
          target="_blank"
          rel="noreferrer"
        >
          Source
        </a>
        <a
          className="utility-button"
          href="/docs"
          target="_blank"
          rel="noreferrer"
        >
          API
        </a>
      </nav>
    </header>
  );
}


function LabOverview({
  models,
  onSelect
}: {
  models: ModelInfo[];
  onSelect: (id: ModelId) => void;
}) {
  return (
    <div className="lab-overview">
      <div className="lab-overview-intro">
        <p className="section-kicker">End-to-end ML engineering</p>
        <h3>Five evaluated ML systems presented as one deployable product.</h3>
        <p>
          The lab keeps training and evaluation methodology inside each project,
          then exposes selected inference paths through one FastAPI layer and one
          React interface.
        </p>
      </div>

      <div className="lab-architecture" aria-label="ML Systems Lab architecture">
        <div>
          <span>Interface</span>
          <strong>React / Vite</strong>
        </div>
        <span className="architecture-arrow" aria-hidden="true">→</span>
        <div>
          <span>Serving layer</span>
          <strong>Unified FastAPI</strong>
        </div>
        <span className="architecture-arrow" aria-hidden="true">→</span>
        <div className="architecture-models">
          <span>Systems</span>
          <strong>RAG · Fraud · Credit · T9 · Spam</strong>
        </div>
      </div>

      <dl className="lab-evidence">
        <div>
          <dt>Evaluation</dt>
          <dd>Held-out metrics and committed machine-readable snapshots</dd>
        </div>
        <div>
          <dt>Serving</dt>
          <dd>Typed REST contracts, Docker and health checks</dd>
        </div>
        <div>
          <dt>Quality</dt>
          <dd>pytest, Ruff, CI and dependency auditing</dd>
        </div>
        <div>
          <dt>Reproducibility</dt>
          <dd>Pinned dependencies and RAG metric-drift verification</dd>
        </div>
      </dl>

      <div className="lab-system-index">
        <div className="lab-system-index-heading">
          <span>System</span>
          <span>Task</span>
          <span>Benchmark</span>
        </div>
        {models.map((model) => (
          <button
            className="lab-system-row"
            key={model.id}
            onClick={() => onSelect(model.id)}
          >
            <strong>{model.name}</strong>
            <span>{model.task}</span>
            <span className="lab-system-benchmark">
              {model.headline_metric} {model.headline_value}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

export function MLSystemsLab() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [active, setActive] = useState<"overview" | ModelId>("overview");
  const [copied, setCopied] = useState(false);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    api<Overview>("/api/overview")
      .then(setOverview)
      .catch((err) => {
        setLoadError(
          err instanceof Error ? err.message : "Unable to connect to the API."
        );
      });
  }, []);

  const models = useMemo(() => {
    const byId = new Map(
      (overview?.models ?? []).map((model) => [model.id, model])
    );
    return serviceOrder
      .map((id) => byId.get(id))
      .filter((model): model is ModelInfo => Boolean(model));
  }, [overview]);

  const activeModel =
    active === "overview"
      ? null
      : models.find((model) => model.id === active) ??
        overview?.models.find((model) => model.id === active) ??
        null;

  async function copyEndpoint() {
    if (!activeModel) return;
    const endpoint = `${window.location.origin}${endpointByModel[activeModel.id]}`;
    await navigator.clipboard.writeText(endpoint);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1200);
  }

  return (
    <section className="portfolio-section lab-section" id="lab">
      <div className="section-heading">
        <p className="section-kicker">Interactive systems</p>
        <h2>ML Systems Lab</h2>
        <p>
          Inspect the evaluation, change model inputs, adjust thresholds and view
          the actual API request/response path.
        </p>
      </div>

      <div className="lab-workbench">
        <aside className="lab-sidebar">
          <div className="sidebar-label">ML Systems</div>
          <nav className="service-list" aria-label="ML systems">
            <button
              className={`service-button ${active === "overview" ? "active" : ""}`}
              onClick={() => {
                setActive("overview");
                setCopied(false);
              }}
            >
              <span className="service-button-copy">
                <strong>Overview</strong>
                <small>Architecture & evaluation</small>
              </span>
            </button>

            {models.map((model) => (
              <button
                key={model.id}
                className={`service-button ${active === model.id ? "active" : ""}`}
                onClick={() => {
                  setActive(model.id);
                  setCopied(false);
                }}
              >
                <span className="service-button-copy">
                  <strong>{model.name}</strong>
                  <small>{model.task}</small>
                </span>
                <span className="service-metric">{model.headline_value}</span>
              </button>
            ))}
          </nav>
        </aside>

        <div className="lab-console">
          {loadError && <div className="error-banner top-error">{loadError}</div>}

          {active === "overview" ? (
            overview ? (
              <LabOverview models={models} onSelect={setActive} />
            ) : (
              <div className="loading-console" aria-label="Loading ML Systems Lab">
                <span className="loading-line" />
                <span className="loading-line short" />
                <span className="loading-panel" />
              </div>
            )
          ) : activeModel ? (
            <div className="system-view" key={activeModel.id}>
              <SystemHeader
                model={activeModel}
                copied={copied}
                onCopy={() => void copyEndpoint()}
              />

              {active === "rag" && <RAGDemo />}
              {active === "fraud" && <RecordDemo kind="fraud" />}
              {active === "credit" && <RecordDemo kind="credit" />}
              {active === "typo" && <TypoDemo />}
              {active === "spam" && <SpamDemo />}
            </div>
          ) : (
            <div className="loading-console" aria-label="Loading model">
              <span className="loading-line" />
              <span className="loading-line short" />
              <span className="loading-panel" />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
