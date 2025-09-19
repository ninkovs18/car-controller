import { useState } from "react";
import { useAuth } from "../context/auth/AuthProvider";

export function RegisterForm({ onSuccess, onCancel }) {
  const { registerWithEmail, setError } = useAuth();
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");
  const [pwd2, setPwd2] = useState("");
  const [busy, setBusy] = useState(false);
  const [localErr, setLocalErr] = useState(null);

  async function onSubmit(e) {
    e.preventDefault();
    setLocalErr(null);
    setError(null);

    if (pwd.length < 6) {
      setLocalErr("Password must be at least 6 characters.");
      return;
    }
    if (pwd !== pwd2) {
      setLocalErr("Passwords do not match.");
      return;
    }

    try {
      setBusy(true);
      await registerWithEmail(email, pwd);
      onSuccess?.();
    } catch (e) {
      setLocalErr(e?.message || "Registration failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="stack" onSubmit={onSubmit}>
      {localErr && <div className="alert error">{localErr}</div>}

      <div>
        <label>Email</label>
        <input
          className="input"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
        />
      </div>

      <div>
        <label>Password</label>
        <input
          className="input"
          type="password"
          value={pwd}
          onChange={(e) => setPwd(e.target.value)}
          placeholder="Minimum 6 characters"
          required
        />
      </div>

      <div>
        <label>Confirm password</label>
        <input
          className="input"
          type="password"
          value={pwd2}
          onChange={(e) => setPwd2(e.target.value)}
          placeholder="Repeat password"
          required
        />
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <button className="button" type="submit" disabled={busy}>
          {busy ? "Creating…" : "Create account"}
        </button>
        <button
          type="button"
          className="button secondary"
          onClick={onCancel}
          disabled={busy}
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
