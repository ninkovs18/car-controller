import React from "react";

export function ResultCard({ title, result, kind }) {
  const cls =
    kind === "ok" ? "result ok" : kind === "warn" ? "result warn" : "result";
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className={cls}>{result}</div>
    </div>
  );
}
