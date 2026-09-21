from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .auth import autenticar, crear_token, requiere_admin, usuario_actual
from .bots import bot_estado_pedido, bot_verificador_primer_pago, bot_verificador_segundo_pago
from .email import enviar_email_confirmacion_pago, enviar_email_pedido_creado
from .models import Pedido, PedidoCreate, Servicio, User
from .payments import PEDIDOS_DB, SERVICIOS_DB, generar_instrucciones_pago

app = FastAPI(title="API negocio r3dm")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def obtener_pedido(pedido_id: int):
    pedido = PEDIDOS_DB.get(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


def puede_ver_pedido(pedido: Pedido, user: User):
    if user.role.value != "admin" and pedido.cliente_email != user.email:
        raise HTTPException(status_code=403, detail="No puedes consultar este pedido")


@app.get("/")
def raiz():
    return {"nombre": "API negocio r3dm", "estado": "ok"}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = autenticar(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"token": crear_token(user), "token_type": "bearer", "role": user.role}


@app.get("/servicios", response_model=List[Servicio])
def listar_servicios(user: User = Depends(usuario_actual)):
    return list(SERVICIOS_DB.values())


@app.post("/pedidos", response_model=Pedido)
def crear_pedido(pedido_data: PedidoCreate, user: User = Depends(usuario_actual)):
    if pedido_data.id in PEDIDOS_DB:
        raise HTTPException(status_code=409, detail="Ya existe un pedido con ese id")
    if pedido_data.servicio_id not in SERVICIOS_DB:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    pedido = Pedido(**pedido_data.model_dump(), cliente_email=user.email)
    PEDIDOS_DB[pedido.id] = pedido
    servicio = SERVICIOS_DB[pedido.servicio_id]
    enviar_email_pedido_creado(pedido, servicio, user.email)
    return pedido


@app.get("/pedidos", response_model=List[Pedido])
def listar_pedidos(user: User = Depends(usuario_actual)):
    if user.role.value == "admin":
        return list(PEDIDOS_DB.values())
    return [p for p in PEDIDOS_DB.values() if p.cliente_email == user.email]


@app.get("/pedidos/{pedido_id}/instrucciones_pago")
def instrucciones_pago(pedido_id: int, user: User = Depends(usuario_actual)):
    pedido = obtener_pedido(pedido_id)
    puede_ver_pedido(pedido, user)
    return generar_instrucciones_pago(pedido)


@app.post("/pedidos/{pedido_id}/confirmar_50_inicial", response_model=Pedido)
def confirmar_50_inicial(pedido_id: int, admin: User = Depends(requiere_admin)):
    pedido = bot_verificador_primer_pago(obtener_pedido(pedido_id), confirmado=True)
    PEDIDOS_DB[pedido_id] = pedido
    enviar_email_confirmacion_pago(pedido, "50% inicial")
    return pedido


@app.post("/pedidos/{pedido_id}/confirmar_50_final", response_model=Pedido)
def confirmar_50_final(pedido_id: int, admin: User = Depends(requiere_admin)):
    pedido = bot_verificador_segundo_pago(obtener_pedido(pedido_id), confirmado=True)
    PEDIDOS_DB[pedido_id] = pedido
    enviar_email_confirmacion_pago(pedido, "50% final")
    return pedido


@app.get("/pedidos/{pedido_id}/estado")
def estado_pedido(pedido_id: int, user: User = Depends(usuario_actual)):
    pedido = obtener_pedido(pedido_id)
    puede_ver_pedido(pedido, user)
    return {"pedido_id": pedido_id, "estado": bot_estado_pedido(pedido)}
