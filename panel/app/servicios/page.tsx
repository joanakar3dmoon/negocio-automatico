"use client";

import { useEffect, useState } from "react";

type Servicio = {
  id: number;
  nombre: string;
  precio_total: number;
};

export default function Servicios() {
  const [items, setItems] = useState<Servicio[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/servicios`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token") || ""}` },
    })
      .then((r) => (r.ok ? r.json() : []))
      .then(setItems);
  }, []);

  return (
    <section>
      <h1>Servicios</h1>
      <div className="grid">
        {items.map((s) => (
          <article className="card" key={s.id}>
            <h2>{s.nombre}</h2>
            <p className="price">{s.precio_total.toFixed(2)} €</p>
            <p>50% inicial: {(s.precio_total / 2).toFixed(2)} €</p>
            <p>50% final a la entrega.</p>
          </article>
        ))}
      </div>
    </section>
  );
}
