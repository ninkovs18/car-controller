import { useAuth } from "../context/auth/AuthProvider";

export function RequireAuth({ children }) {
  const { user, authLoading, loginWithGoogle } = useAuth();

  if (authLoading)
    return (
      <div className="card">
        <p>Loading…</p>
      </div>
    );

  if (!user) {
    return (
      <div className="card" style={{ maxWidth: 420, margin: "60px auto" }}>
        <h2>Sign in required</h2>
        <p className="muted">
          Please sign in with Google to use Vehicle Controller.
        </p>
        <button className="button" onClick={loginWithGoogle}>
          Sign in with Google
        </button>
      </div>
    );
  }
  return children;
}
