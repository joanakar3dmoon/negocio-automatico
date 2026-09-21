import Link from "next/link";

export default function Home() {
  return (
    <section className="hero">
      <p className="eyebrow">NEGOCIO AUTOMÁTICO</p>
      <h1>Servicios creativos, pagos claros.</h1>
      <p>Gestiona tus servicios con un prepago del 50% y el 50% restante a la entrega final.</p>
      <div className="actions">
        <Link className="button" href="/login">Iniciar sesión</Link>
        <Link className="button secondary" href="/servicios">Ver servicios</Link>
      </div>
    </section>
  );
}
