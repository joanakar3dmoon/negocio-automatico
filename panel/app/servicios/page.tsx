"use client";
import { useEffect, useState } from "react";

export default function ServiciosPage() {
  const [servicios, setServicios] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const base = process.env.NEXT_PUBLIC_API_URL || "";

  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch(`${base}/servicios`, { headers: { Authorization: `Bearer ${token}` } })
      .then(async res => res.ok ? res.json() : Promise.reject(new Error("Sesión no válida")))
      .then(setServicios).catch(error => setMensaje(error.message));
  }, [base]);

  const crearPedido = async (servicio) => {
    const token = localStorage.getItem("token");
    const cliente_email = localStorage.getItem("email");
    const pedido = { id: Date.now(), servicio_id: servicio.id, cliente_email, metodo_pago: "bizum" };
    const res = await fetch(`${base}/pedidos`, { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify(pedido) });
    setMensaje(res.ok ? `Pedido ${pedido.id} creado. Consulta sus instrucciones en Pagos.` : "No se pudo crear el pedido");
  };

  return (
    <main>
      <h2>Servicios disponibles</h2>
      {mensaje && <p>{mensaje}</p>}
      <ul>{servicios.map(s => <li key={s.id}>{s.nombre} — {s.precio_total} € <button onClick={() => crearPedido(s)}>Crear pedido</button></li>)}</ul>
    </main>
  );
}