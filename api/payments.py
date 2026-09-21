from typing import Dict

from .models import MetodoPago, Pedido, Servicio

SERVICIOS_DB: Dict[int, Servicio] = {
    1: Servicio(id=1, nombre="Producción musical completa", precio_total=1000.0),
    2: Servicio(id=2, nombre="Mezcla y máster", precio_total=600.0),
}

PEDIDOS_DB: Dict[int, Pedido] = {}

DATOS_PAGO_PERSONAL = {
    MetodoPago.CAIXABANK: {
        "tipo": "transferencia",
        "iban": "ES00 0000 0000 0000 0000 0000",
        "titular": "Tu nombre personal",
        "concepto": "Servicio r3dm",
    },
    MetodoPago.REVOLUT: {
        "tipo": "transferencia",
        "iban": "LT00 0000 0000 0000 0000",
        "titular": "Tu nombre personal",
        "concepto": "Servicio r3dm",
    },
    MetodoPago.BIZUM: {
        "tipo": "bizum",
        "telefono": "+34 600 000 000",
        "concepto": "Servicio r3dm",
    },
    MetodoPago.TARJETA_CREDITO: {
        "tipo": "tarjeta",
        "pasarela": "Introduce manualmente los datos en tu TPV o enlace de cobro",
    },
}


def calcular_importes(servicio: Servicio):
    mitad = round(servicio.precio_total * 0.5, 2)
    return {"primer_pago": mitad, "segundo_pago": round(servicio.precio_total - mitad, 2)}


def generar_instrucciones_pago(pedido: Pedido):
    servicio = SERVICIOS_DB[pedido.servicio_id]
    importes = calcular_importes(servicio)
    return {
        "servicio": servicio.nombre,
        "precio_total": servicio.precio_total,
        "primer_pago_50": importes["primer_pago"],
        "segundo_pago_50": importes["segundo_pago"],
        "metodo": pedido.metodo_pago,
        "datos_pago_personal": DATOS_PAGO_PERSONAL[pedido.metodo_pago],
        "regla": "50% prepago antes de empezar, 50% a la entrega final.",
    }
