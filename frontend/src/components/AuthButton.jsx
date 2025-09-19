import { useAuth } from "../context/auth/AuthProvider";

export function AuthButton() {
  const { user, loadingAuth, loginWithGoogle, logout } = useAuth();

  if (loadingAuth) {
    return <span style={{ opacity: 0.7 }}>Checking…</span>;
  }

  if (!user) {
    return (
      <button className="button secondary" onClick={loginWithGoogle}>
        Sign in
      </button>
    );
  }

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <span style={{ fontSize: 12, color: "var(--muted)" }}>
        {user.displayName || user.email}
      </span>
      <button className="button secondary" onClick={logout}>
        Sign out
      </button>
    </div>
  );
}
