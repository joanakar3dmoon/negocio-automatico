"use client";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");

  const entrar = async () => {
    const data = new URLSearchParams();
    data.append("username", email);
    data.append("password", pass);

    const res = await fetch("/api/login", {
      method: "POST",
      body: data
    });

    const json = await res.json();
    localStorage.setItem("token", json.token);
    window.location.href = "/servicios";
  };

  return (
    <main>
      <h2>Login</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" onChange={e => setPass(e.target.value)} />
      <button onClick={entrar}>Entrar</button>
    </main>
  );
}