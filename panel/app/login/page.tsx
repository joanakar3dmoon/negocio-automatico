"use client";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [error, setError] = useState("");

  const entrar = async (event) => {
    event.preventDefault();
    setError("");
    const data = new URLSearchParams({ username: email, password: pass });
    const base = process.env.NEXT_PUBLIC_API_URL || "";
    const res = await fetch(`${base}/login`, { method: "POST", body: data });
    const json = await res.json();
    if (!res.ok) {
      setError(json.detail || "No se pudo iniciar sesión");
      return;
    }
    localStorage.setItem("token", json.token);
    localStorage.setItem("role", json.role);
    localStorage.setItem("email", json.email);
    window.location.href = "/servicios";
  };

  return (
    <main>
      <h2>Login</h2>
      <form onSubmit={entrar}>
        <input required placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input required placeholder="Password" type="password" value={pass} onChange={e => setPass(e.target.value)} />
        <button type="submit">Entrar</button>
      </form>
      {error && <p role="alert">{error}</p>}
    </main>
  );
}