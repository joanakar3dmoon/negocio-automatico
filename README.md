# negocio-automatico

Aplicación con API FastAPI y panel Next.js para gestionar servicios, pedidos y pagos personales divididos en 50% inicial y 50% final. No integra Stripe ni PayPal.

## API local

Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
uvicorn api.main:app --reload
```

La documentación está en `http://localhost:8000/docs` y la comprobación de salud en `/health`.

Credenciales de demostración: `admin@r3dm.com` / `admin123` y `cliente@r3dm.com` / `cliente123`. Cámbialas antes de usar el sistema en producción y define `JWT_SECRET`.

## Panel local

```bash
cd panel
npm install
npm run dev
```

Para conectar el panel con una API remota, define `NEXT_PUBLIC_API_URL` en Vercel, por ejemplo `https://TU-API.onrender.com`. Para desarrollo local puede omitirse si el panel y la API están detrás del mismo proxy.

## Despliegue

### Render

Crea un Blueprint seleccionando este repositorio. `render.yaml` publica la API con `uvicorn api.main:app` y conserva el dashboard estático existente. Define `CORS_ORIGINS` con la URL exacta del panel de Vercel, por ejemplo `https://panel-r3dm.vercel.app`.

### Vercel

Crea un proyecto Vercel apuntando al directorio `panel` (o configura `Root Directory` como `panel`). El archivo `panel/vercel.json` ya define Next.js. Añade `NEXT_PUBLIC_API_URL` con la URL pública de Render y ejecuta el despliegue.

## Flujo de pagos

1. El cliente inicia sesión y crea un pedido desde Servicios.
2. En Pagos consulta CaixaBank, Revolut, Bizum o tarjeta manual.
3. El admin confirma manualmente el 50% inicial cuando lo recibe.
4. El admin confirma manualmente el 50% final al entregar el servicio.

Los datos actuales de pago son placeholders y deben sustituirse por los datos reales mediante variables seguras antes de publicar.