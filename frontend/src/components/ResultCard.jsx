import React from "react";

export function ResultCard({ title, kind, primary, secondary }) {
  const cls =
    kind === "ok" ? "result ok" : kind === "warn" ? "result warn" : "result";

  return (
    <div className="card">
      <h2>{title}</h2>
      <div className={cls}>
        <div className="result-primary">{primary}</div>
        {secondary && <div className="result-secondary">{secondary}</div>}
      </div>
    </div>
  );
}
