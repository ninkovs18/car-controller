import { useState } from "react";
import { useAuth } from "../context/auth/AuthProvider";
import { RegisterForm } from "./RegisterForm";

export function RequireAuth({ children }) {
  const { user, busy, loginWithGoogle, loginWithEmail, error, setError } =
    useAuth();
  const [view, setView] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  if (busy)
    return (
      <div className="container">
        <div className="card">
          <p>Loading…</p>
        </div>
      </div>
    );

  if (user) return children;

  async function onSubmit(e) {
    e.preventDefault();
    try {
      await loginWithEmail(email, password);
    } catch (e) {
      setError(e?.message || "Login failed");
    }
  }

  return (
    <main className="container" style={{ maxWidth: 480 }}>
      <div className="card">
        <h2>{view === "login" ? "Sign in" : "Create account"}</h2>
        {error && <div className="alert error">{error}</div>}

        {view === "login" ? (
          <>
            <form className="stack" onSubmit={onSubmit}>
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
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Your password"
                  required
                />
              </div>

              <button className="button" type="submit">
                Sign in
              </button>
            </form>

            <div
              style={{
                margin: "12px 0",
                textAlign: "center",
                color: "var(--muted)",
              }}
            >
              — or —
            </div>

            <button
              className="button secondary google-login"
              onClick={loginWithGoogle}
              style={{ margin: "0 auto" }}
            >
              <img
                src="https://www.svgrepo.com/show/475656/google-color.svg"
                alt="Google"
                style={{ width: 20, height: 20, marginRight: 8 }}
              />
              Continue with Google
            </button>

            <p style={{ textAlign: "center", marginTop: "10px" }}>
              Don’t have an account?{" "}
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  setError(null);
                  setView("register");
                }}
              >
                Create one
              </a>
            </p>
          </>
        ) : (
          <>
            <RegisterForm
              onSuccess={() => setView("login")}
              onCancel={() => setView("login")}
            />
            <p style={{ marginTop: 12 }}>
              Already have an account?{" "}
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  setError(null);
                  setView("login");
                }}
              >
                Sign in
              </a>
            </p>
          </>
        )}
      </div>
    </main>
  );
}
