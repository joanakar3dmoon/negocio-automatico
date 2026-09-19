import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .models import Pedido, Servicio
from .auth import autenticar, crear_token, usuario_actual, requiere_admin
from .payments import SERVICIOS_DB, PEDIDOS_DB, generar_instrucciones_pago
from .bots import bot_verificador_primer_pago, bot_verificador_segundo_pago, bot_estado_pedido

app = FastAPI(title="API negocio r3dm")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = autenticar(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"token": crear_token(user), "role": user.role, "email": user.email}

@app.get("/servicios", response_model=List[Servicio])
def listar_servicios(user=Depends(usuario_actual)):
    return list(SERVICIOS_DB.values())

@app.post("/pedidos", response_model=Pedido)
def crear_pedido(pedido: Pedido, user=Depends(usuario_actual)):
    if pedido.servicio_id not in SERVICIOS_DB:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    if pedido.cliente_email != user.email and user.role.value != "admin":
        raise HTTPException(status_code=403, detail="No puedes crear pedidos para otro cliente")
    PEDIDOS_DB[pedido.id] = pedido
    return pedido

@app.get("/pedidos/{pedido_id}/instrucciones_pago")
def instrucciones_pago(pedido_id: int, user=Depends(usuario_actual)):
    pedido = PEDIDOS_DB.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.cliente_email != user.email and user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Sin acceso a este pedido")
    return generar_instrucciones_pago(pedido)

@app.post("/pedidos/{pedido_id}/confirmar_50_inicial", response_model=Pedido)
def confirmar_50_inicial(pedido_id: int, admin=Depends(requiere_admin)):
    pedido = PEDIDOS_DB.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    PEDIDOS_DB[pedido_id] = bot_verificador_primer_pago(pedido, confirmado=True)
    return PEDIDOS_DB[pedido_id]

@app.post("/pedidos/{pedido_id}/confirmar_50_final", response_model=Pedido)
def confirmar_50_final(pedido_id: int, admin=Depends(requiere_admin)):
    pedido = PEDIDOS_DB.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    PEDIDOS_DB[pedido_id] = bot_verificador_segundo_pago(pedido, confirmado=True)
    return PEDIDOS_DB[pedido_id]

@app.get("/pedidos/{pedido_id}/estado")
def estado_pedido(pedido_id: int, user=Depends(usuario_actual)):
    pedido = PEDIDOS_DB.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.cliente_email != user.email and user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Sin acceso a este pedido")
    return {"estado": bot_estado_pedido(pedido), "pedido": pedido}