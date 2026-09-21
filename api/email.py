import os
from typing import Any, Dict

import requests

EMAILJS_SERVICE_ID = os.getenv("EMAILJS_SERVICE_ID", "service_h1n7lcs")
EMAILJS_TEMPLATE_ID = os.getenv("EMAILJS_TEMPLATE_ID", "template_4ba2t5l")
EMAILJS_PUBLIC_KEY = os.getenv("EMAILJS_PUBLIC_KEY", "cuCvmbTw60MTSMoNS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@r3dm.com")
EMAILJS_API_URL = "https://api.emailjs.com/api/v1.0/email/send"


def _enviar_email(to_email: str, subject: str, template_params: Dict[str, Any]):
    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_PUBLIC_KEY,
        "template_params": {
            "to_email": to_email,
            "subject": subject,
            **template_params,
        },
    }
    try:
        response = requests.post(EMAILJS_API_URL, json=payload, timeout=15)
        response.raise_for_status()
        return {"ok": True, "status_code": response.status_code}
    except Exception as exc:  # pragma: no cover - depende de servicio externo
        return {"ok": False, "error": str(exc)}


def enviar_email_pedido_creado(pedido, servicio, cliente_email: str):
    params = {
        "order_id": pedido.id,
        "customer_email": cliente_email,
        "servicio_nombre": servicio.nombre,
        "precio_total": f"{servicio.precio_total:.2f}",
        "metodo_pago": pedido.metodo_pago.value,
        "estado": "Pedido creado",
        "regla": "50% prepago antes de empezar, 50% a la entrega final.",
    }
    for destino in [cliente_email, ADMIN_EMAIL]:
        _enviar_email(destino, f"Pedido #{pedido.id} creado", params)


def enviar_email_confirmacion_pago(pedido, tipo_pago: str):
    servicio = pedido if hasattr(pedido, "nombre") else None
    params = {
        "order_id": pedido.id,
        "customer_email": pedido.cliente_email,
        "tipo_pago": tipo_pago,
        "estado": f"Confirmado {tipo_pago}",
        "metodo_pago": pedido.metodo_pago.value,
    }
    for destino in [pedido.cliente_email, ADMIN_EMAIL]:
        _enviar_email(destino, f"Pago {tipo_pago} confirmado - Pedido #{pedido.id}", params)
