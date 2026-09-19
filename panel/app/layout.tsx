export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <nav>
          <a href="/">Inicio</a> | <a href="/servicios">Servicios</a> | <a href="/pagos">Pagos</a> | <a href="/admin">Admin</a>
        </nav>
        {children}
      </body>
    </html>
  );
}