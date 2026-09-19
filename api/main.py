from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from .models import Servicio, Pedido
from .auth import autenticar, crear_token, usuario_actual, requiere_admin
from .payments import SERVICIOS_DB, PEDIDOS_DB, generar_instrucciones_pago
from .bots import bot_verificador_primer_pago, bot_verificador_segundo_pago, bot_estado_pedido

app = FastAPI(title="API negocio r3dm")

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = autenticar(form.username, form.password)
    if not user:
        return {"error": "Credenciales incorrectas"}
    return {"token": crear_token(user)}

@app.get("/servicios", response_model=List[Servicio])
def listar_servicios(user=Depends(usuario_actual)):
    return list(SERVICIOS_DB.values())

@app.post("/pedidos", response_model=Pedido)
def crear_pedido(pedido: Pedido, user=Depends(usuario_actual)):
    PEDIDOS_DB[pedido.id] = pedido
    return pedido

@app.get("/pedidos/{pedido_id}/instrucciones_pago")
def instrucciones_pago(pedido_id: int, user=Depends(usuario_actual)):
    pedido = PEDIDOS_DB[pedido_id]
    return generar_instrucciones_pago(pedido)

@app.post("/pedidos/{pedido_id}/confirmar_50_inicial", response_model=Pedido)
def confirmar_50_inicial(pedido_id: int, admin=Depends(requiere_admin)):
    pedido = PEDIDOS_DB[pedido_id]
    pedido = bot_verificador_primer_pago(pedido, confirmado=True)
    PEDIDOS_DB[pedido_id] = pedido
    return pedido

@app.post("/pedidos/{pedido_id}/confirmar_50_final", response_model=Pedido)
def confirmar_50_final(pedido_id: int, admin=Depends(requiere_admin)):
    pedido = PEDIDOS_DB[pedido_id]
    pedido = bot_verificador_segundo_pago(pedido, confirmado=True)
    PEDIDOS_DB[pedido_id] = pedido
    return pedido

@app.get("/pedidos/{pedido_id}/estado")
def estado_pedido(pedido_id: int, user=Depends(usuario_actual)):
    pedido = PEDIDOS_DB[pedido_id]
    return {"estado": bot_estado_pedido(pedido)}