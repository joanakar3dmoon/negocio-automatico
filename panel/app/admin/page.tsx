"use client";

import { useEffect, useState } from "react";

type Pedido = {
  id: number;
  pagado_50_inicial: boolean;
  pagado_50_final: boolean;
  cliente_email: string;
};

export default function Admin() {
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const headers = {
    Authorization: `Bearer ${typeof window !== "undefined" ? localStorage.getItem("token") || "" : ""}`,
  };

  useEffect(() => {
    fetch(`${api}/pedidos`, { headers }).then((r) => (r.ok ? r.json() : [])).then(setPedidos);
  }, []);

  async function confirmar(id: number, fase: "inicial" | "final") {
    await fetch(`${api}/pedidos/${id}/confirmar_50_${fase}`, {
      method: "POST",
      headers,
    });
    const updated = await fetch(`${api}/pedidos`, { headers }).then((r) => r.json());
    setPedidos(updated);
  }

  return (
    <section>
      <h1>Administración</h1>
      {pedidos.length === 0 && <p>No hay pedidos o la sesión no tiene permisos.</p>}
      {pedidos.map((p) => (
        <article className="card" key={p.id}>
          <h2>Pedido #{p.id}</h2>
          <p>{p.cliente_email}</p>
          <p>
            Inicial: {p.pagado_50_inicial ? "confirmado" : "pendiente"} · Final: {p.pagado_50_final ? "confirmado" : "pendiente"}
          </p>
          <div className="actions">
            {!p.pagado_50_inicial && (
              <button className="button" onClick={() => confirmar(p.id, "inicial")}>
                Confirmar 50% inicial
              </button>
            )}
            {!p.pagado_50_final && (
              <button className="button secondary" onClick={() => confirmar(p.id, "final")}>
                Confirmar 50% final
              </button>
            )}
          </div>
        </article>
      ))}
    </section>
  );
}
