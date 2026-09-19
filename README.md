# negocio-automatico

Aplicación con API FastAPI y panel Next.js para gestionar servicios, pedidos y pagos personales divididos en 50% inicial y 50% final. No integra Stripe ni PayPal.

## Variables de despliegue

### API en Render

Configura estas variables en el servicio de la API:

```text
JWT_SECRET=una_cadena_aleatoria_larga_y_segura
CORS_ORIGINS=https://tu-panel.vercel.app
```

`JWT_SECRET` debe ser un secreto real generado en Render y no debe guardarse en GitHub. `CORS_ORIGINS` debe contener la URL pública exacta del panel de Vercel.

### Panel en Vercel

Configura esta variable en el proyecto del panel:

```text
NEXT_PUBLIC_API_URL=https://tu-api.onrender.com
```

Debe apuntar a la URL pública real del servicio FastAPI en Render, sin añadir `/login` ni otra ruta.

Los archivos `api/.env.example` y `panel/.env.example` contienen únicamente plantillas seguras; no contienen secretos reales.

## API local

Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
uvicorn api.main:app --reload
```

La documentación está en `http://localhost:8000/docs` y la comprobación de salud en `/health`.

Credenciales de demostración: `admin@r3dm.com` / `admin123` y `cliente@r3dm.com` / `cliente123`. Cámbialas antes de usar el sistema en producción.

## Panel local

```bash
cd panel
npm install
npm run dev
```

## Despliegue

En Vercel, configura el directorio raíz del proyecto como `panel` y añade `NEXT_PUBLIC_API_URL`. En Render, despliega la API usando `render.yaml` y define `JWT_SECRET` y `CORS_ORIGINS` en Environment.

## Flujo de pagos

1. El cliente inicia sesión y crea un pedido desde Servicios.
2. En Pagos consulta CaixaBank, Revolut, Bizum o tarjeta manual.
3. El admin confirma manualmente el 50% inicial cuando lo recibe.
4. El admin confirma manualmente el 50% final al entregar el servicio.

Los datos actuales de pago son placeholders y deben sustituirse por datos reales mediante variables seguras antes de publicar.