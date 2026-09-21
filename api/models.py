from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    ADMIN = "admin"
    CLIENTE = "cliente"


class User(BaseModel):
    email: str
    password: str
    role: Role


class MetodoPago(str, Enum):
    CAIXABANK = "caixabank_transferencia"
    REVOLUT = "revolut_transferencia"
    BIZUM = "bizum"
    TARJETA_CREDITO = "tarjeta_credito"


class Servicio(BaseModel):
    id: int
    nombre: str
    precio_total: float


class Pedido(BaseModel):
    id: int
    servicio_id: int
    cliente_email: str
    metodo_pago: MetodoPago
    pagado_50_inicial: bool = False
    pagado_50_final: bool = False


class PedidoCreate(BaseModel):
    id: int = Field(gt=0)
    servicio_id: int = Field(gt=0)
    metodo_pago: MetodoPago
