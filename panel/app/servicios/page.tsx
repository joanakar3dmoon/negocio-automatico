"use client";
import { useEffect, useState } from "react";

export default function ServiciosPage() {
  const [servicios, setServicios] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("/api/servicios", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setServicios);
  }, []);

  return (
    <main>
      <h2>Servicios disponibles</h2>
      <ul>
        {servicios.map(s => (
          <li key={s.id}>{s.nombre} — {s.precio_total} €</li>
        ))}
      </ul>
    </main>
  );
}