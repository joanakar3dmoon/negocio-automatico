# API negocio-automatico

La API usa FastAPI y almacenamiento temporal en memoria para la demo. Los pedidos se pierden al reiniciar el proceso; para producción debe añadirse una base de datos y migraciones.

Ejecuta desde la raíz con `uvicorn api.main:app --reload`.