"use client";
import { useState } from "react";

export default function PagosPage() {
  const [pedidoId, setPedidoId] = useState("");
  const [info, setInfo] = useState(null);
  const [error, setError] = useState("");
  const base = process.env.NEXT_PUBLIC_API_URL || "";

  const cargar = async () => {
    setError("");
    const res = await fetch(`${base}/pedidos/${pedidoId}/instrucciones_pago`, { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    const json = await res.json();
    if (!res.ok) return setError(json.detail || "Pedido no encontrado");
    setInfo(json);
  };

  return <main><h2>Pagos personales</h2><input value={pedidoId} onChange={e => setPedidoId(e.target.value)} placeholder="ID pedido" /><button onClick={cargar}>Ver instrucciones</button>{error && <p>{error}</p>}{info && <section><h3>{info.servicio}</h3><p>Prepago 50%: {info.primer_pago_50} €</p><p>Final 50%: {info.segundo_pago_50} €</p><pre>{JSON.stringify(info.datos_pago_personal, null, 2)}</pre></section>}</main>;
}