"use client";
import { useState } from "react";

export default function Admin() {
  const [pedidoId, setPedidoId] = useState("");
  const [mensaje, setMensaje] = useState("");
  const base = process.env.NEXT_PUBLIC_API_URL || "";

  const confirmar = async (tipo) => {
    const res = await fetch(`${base}/pedidos/${pedidoId}/${tipo}`, { method: "POST", headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
    const json = await res.json();
    setMensaje(res.ok ? "Pago confirmado correctamente" : (json.detail || "No autorizado"));
  };

  return <main><h2>Panel Admin</h2><input placeholder="ID pedido" value={pedidoId} onChange={e => setPedidoId(e.target.value)} /><button onClick={() => confirmar("confirmar_50_inicial")}>Confirmar 50% inicial</button><button onClick={() => confirmar("confirmar_50_final")}>Confirmar 50% final</button>{mensaje && <p>{mensaje}</p>}</main>;
}