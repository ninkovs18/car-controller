import { useState } from "react";

export function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  async function onCopy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    } catch {
      // ignore
    }
  }
  return (
    <button className="button secondary copy" type="button" onClick={onCopy}>
      {copied ? "Copied" : "Copy"}
    </button>
  );
}
