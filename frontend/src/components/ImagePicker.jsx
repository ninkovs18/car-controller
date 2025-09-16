import { useState, useEffect, useRef } from "react";

export function ImagePicker({
  file,
  onFile,
  label = "Choose image",
  accept = "image/*",
}) {
  const inputRef = useRef(null);
  const [preview, setPreview] = useState(null);

  useEffect(() => {
    if (!file) {
      setPreview(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  return (
    <div className="stack">
      <div className="row">
        <div>
          <input
            ref={inputRef}
            className="input"
            type="file"
            accept={accept}
            onChange={(e) => {
              const f = e.currentTarget.files?.[0] ?? null;
              onFile(f);
            }}
          />
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button
            className="button secondary"
            type="button"
            onClick={() => inputRef.current?.click()}
          >
            {label}
          </button>
          {file && (
            <button
              className="button secondary"
              type="button"
              onClick={() => onFile(null)}
            >
              Remove
            </button>
          )}
        </div>
      </div>

      <div className="preview">
        {preview ? (
          <img src={preview} alt="preview" />
        ) : (
          <span>No image selected</span>
        )}
      </div>
    </div>
  );
}
