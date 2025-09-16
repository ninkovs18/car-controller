import { useState } from "react";
import { ImagePicker } from "../ImagePicker";
import { ResultCard } from "../ResultCard";
import { CopyButton } from "../CopyButton";
import { readVIN } from "../../services/api";

export function SectionVIN() {
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
      const res = await readVIN(file);
      console.log(res);
      // if (res.type !== "vin") throw new Error("API did not return VIN.");
      setValue(res);
    } catch (err) {
      setError(err?.message ?? "Failed to read VIN.");
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
      <h2>Read VIN</h2>
      <p>Upload the image containing the vehicle’s VIN (17 characters).</p>

      <form className="stack" onSubmit={onSubmit}>
        <ImagePicker file={file} onFile={setFile} />

        {error && <div className="alert error">{error}</div>}

        <div style={{ display: "flex", gap: 8 }}>
          <button className="button" type="submit" disabled={loading}>
            {loading ? "Reading…" : "Read VIN"}
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
            title="VIN"
            result={
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
