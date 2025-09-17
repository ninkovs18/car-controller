import { useState } from "react";
import { ImagePicker } from "../ImagePicker";
import { ResultCard } from "../ResultCard";
import { analyzeImage } from "../../services/api";
import { OPTIONS, OPTIONS_DISPLAY, QUESTION_MAP } from "./options.js";

export function SectionAnalyze() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [angle, setAngle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [answer, setAnswer] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setError(null);
    setAnswer(null);

    if (!file) {
      setError("Please choose an image.");
      return;
    }
    if (!question) {
      setError("Please select an angle.");
      return;
    }

    try {
      setLoading(true);
      const res = await analyzeImage(question, file);
      setAnswer(res);
    } catch (err) {
      setError(err?.message ?? "Failed to analyze.");
    } finally {
      setLoading(false);
    }
  }

  function handleSelectOption(e) {
    e.preventDefault();
    setAngle(e.target.value);
    setQuestion(QUESTION_MAP[e.target.value]);
  }

  function onReset() {
    setFile(null);
    setQuestion("");
    setAngle("");
    setError(null);
    setAnswer(null);
  }

  const kind =
    answer?.result === "Correct"
      ? "ok"
      : answer?.result === "Incorrect"
      ? "warn"
      : "neutral";

  return (
    <div className="card">
      <h2>Analyze angle</h2>
      <p>Upload a vehicle image and select the expected angle.</p>

      <form className="stack" onSubmit={onSubmit}>
        <ImagePicker file={file} onFile={setFile} />

        <div>
          <label htmlFor="expected-angle-select">Expected angle</label>
          <select
            id="expected-angle-select"
            value={angle}
            onChange={handleSelectOption}
          >
            <option value="">Select angle…</option>
            {OPTIONS.map((opt) => (
              <option key={opt} value={opt}>
                {OPTIONS_DISPLAY[opt]}
              </option>
            ))}
          </select>
        </div>

        {error && <div className="alert error">{error}</div>}

        <div style={{ display: "flex", gap: 8 }}>
          <button className="button" type="submit" disabled={loading}>
            {loading ? "Analyzing…" : "Analyze"}
          </button>
          <button
            className="button secondary"
            type="button"
            onClick={onReset}
            disabled={loading}
          >
            Reset
          </button>
        </div>
        {loading && <p>Processing request. This may take up to a minute.</p>}
        {answer && (
          <ResultCard
            title="Result"
            kind={kind}
            primary={answer.result}
            secondary={answer.message}
          />
        )}
      </form>
    </div>
  );
}
