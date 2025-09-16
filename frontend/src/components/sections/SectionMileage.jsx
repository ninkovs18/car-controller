import { useState } from "react";
import { ImagePicker } from "../ImagePicker";
import { ResultCard } from "../ResultCard";
import { CopyButton } from "../CopyButton";
import { readMileage } from "../../services/api";

export function SectionMileage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [value, setValue] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setError(null);
    setValue(null);
    if (!file) {
      setError("Please choose an image.");
      return;
    }

    try {
      setLoading(true);
      const res = await readMileage(file);
      // if (res.type !== "mileage")
      //   throw new Error("API did not return mileage.");
      setValue(res);
    } catch (err) {
      setError(err?.message ?? "Failed to read mileage.");
    } finally {
      setLoading(false);
    }
  }

  function onReset() {
    setFile(null);
    setError(null);
    setValue(null);
  }

  return (
    <div className="card">
      <h2>Read mileage</h2>
      <p>Upload a photo of the odometer. The API returns a numeric value.</p>

      <form className="stack" onSubmit={onSubmit}>
        <ImagePicker file={file} onFile={setFile} />

        {error && <div className="alert error">{error}</div>}

        <div style={{ display: "flex", gap: 8 }}>
          <button className="button" type="submit" disabled={loading}>
            {loading ? "Reading…" : "Read mileage"}
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
        {value && (
          <ResultCard
            title="Mileage"
            primary={
              <div>
                <strong>{value}</strong>
                <CopyButton text={value} />
              </div>
            }
            kind="ok"
          />
        )}
      </form>
    </div>
  );
}
