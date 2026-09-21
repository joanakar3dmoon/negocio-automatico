from .models import Pedido


def bot_verificador_primer_pago(pedido: Pedido, confirmado: bool):
    if confirmado:
        pedido.pagado_50_inicial = True
    return pedido


def bot_verificador_segundo_pago(pedido: Pedido, confirmado: bool):
    if confirmado:
        pedido.pagado_50_final = True
    return pedido


def bot_estado_pedido(pedido: Pedido):
    if not pedido.pagado_50_inicial:
        return "Esperando prepago 50% para iniciar el servicio."
    if not pedido.pagado_50_final:
        return "Servicio en curso. Pendiente 50% final."
    return "Servicio completado y pagado."
