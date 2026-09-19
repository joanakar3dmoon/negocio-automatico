# API profesional PostgreSQL — Negocio Automático

La API FastAPI usa PostgreSQL mediante SQLAlchemy. Los datos dejan de vivir en listas de memoria y sobreviven a reinicios y despliegues.

## Arranque local

```bash
createdb negocio_automatico
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/negocio_automatico
uvicorn main:app --reload
```

Documentación interactiva: `http://localhost:8000/docs`

## Despliegue en Render

1. Crea un Blueprint desde `render.yaml`.
2. Render crea la API y la base PostgreSQL.
3. La variable `DATABASE_URL` se conecta automáticamente.
4. Comprueba `https://TU-SERVICIO.onrender.com/health`.

Incluye endpoints para leads, webs, pagos, retiros, bots, métricas, cerebros y usuarios. Antes de manejar dinero real añade autenticación, autorización por roles, migraciones Alembic, auditoría, rate limiting y un proveedor de pagos real. No guardes claves privadas, IBAN ni secretos en el frontend.
