"use client";

import { FormEvent, useState } from "react";

export default function Login() {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/login`, {
      method: "POST",
      body: data,
    });

    const result = await response.json();
    if (response.ok) {
      localStorage.setItem("token", result.token);
      setMessage("Sesión iniciada correctamente.");
    } else {
      setMessage(result.detail || "No se pudo iniciar sesión.");
    }
  }

  return (
    <section className="card narrow">
      <h1>Iniciar sesión</h1>
      <form onSubmit={submit}>
        <label>
          Email
          <input name="username" type="email" required />
        </label>
        <label>
          Contraseña
          <input name="password" type="password" required />
        </label>
        <button className="button">Entrar</button>
      </form>
      {message && <p>{message}</p>}
    </section>
  );
}
