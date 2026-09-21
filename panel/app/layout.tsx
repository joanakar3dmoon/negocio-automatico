import type { Metadata } from "next";
import Link from "next/link";
import "./styles.css";

export const metadata: Metadata = {
  title: "Negocio r3dm",
  description: "Panel de servicios y pagos",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body>
        <header>
          <strong>negocio r3dm</strong>
          <nav>
            <Link href="/">Inicio</Link>
            <Link href="/servicios">Servicios</Link>
            <Link href="/pagos">Pagos</Link>
            <Link href="/admin">Admin</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
