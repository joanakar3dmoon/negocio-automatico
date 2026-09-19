"use client";
import { useState } from "react";

export default function Admin() {
  const [pedidoId, setPedidoId] = useState("");

  const confirmar = async (tipo) => {
    const token = localStorage.getItem("token");
    await fetch(`/api/pedidos/${pedidoId}/${tipo}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });
  };

  return (
    <main>
      <h2>Panel Admin</h2>
      <input placeholder="ID pedido" onChange={e => setPedidoId(e.target.value)} />
      <button onClick={() => confirmar("confirmar_50_inicial")}>Confirmar 50% inicial</button>
      <button onClick={() => confirmar("confirmar_50_final")}>Confirmar 50% final</button>
    </main>
  );
}