from datetime import datetime
from typing import Generator
import os

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/negocio_automatico")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(160), index=True)
    sector: Mapped[str] = mapped_column(String(120), index=True)
    ciudad: Mapped[str] = mapped_column(String(120), index=True)
    estado: Mapped[str] = mapped_column(String(40), default="nuevo", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

class Website(Base):
    __tablename__ = "websites"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente: Mapped[str] = mapped_column(String(160), index=True)
    dominio: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    estado: Mapped[str] = mapped_column(String(40), default="en_proceso", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente: Mapped[str] = mapped_column(String(160), index=True)
    cantidad: Mapped[float] = mapped_column(Float)
    metodo: Mapped[str] = mapped_column(String(60))
    estado: Mapped[str] = mapped_column(String(40), default="pendiente", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    origen: Mapped[str] = mapped_column(String(160))
    cantidad: Mapped[float] = mapped_column(Float)
    destino: Mapped[str] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(40), default="solicitado", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Bot(Base):
    __tablename__ = "bots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    zona: Mapped[str] = mapped_column(String(120), default="España")
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Negocio Automático API", version="1.0.0", description="API profesional con PostgreSQL")

class LeadIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=160)
    sector: str = Field(min_length=2, max_length=120)
    ciudad: str = Field(min_length=2, max_length=120)

class LeadOut(LeadIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    estado: str
    created_at: datetime

class WebsiteIn(BaseModel):
    cliente: str = Field(min_length=2, max_length=160)
    dominio: str = Field(min_length=3, max_length=255)
    estado: str = "en_proceso"

class WebsiteOut(WebsiteIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class PaymentIn(BaseModel):
    cliente: str = Field(min_length=2, max_length=160)
    cantidad: float = Field(gt=0)
    metodo: str = Field(min_length=2, max_length=60)

class WithdrawalIn(BaseModel):
    origen: str = Field(min_length=2, max_length=160)
    cantidad: float = Field(gt=0)
    destino: str = Field(min_length=2, max_length=255)

class UserIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=160)
    email: EmailStr

def db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def seed_bots(session: Session) -> None:
    if session.scalar(select(func.count(Bot.id))) == 0:
        session.add_all([Bot(nombre="cazador"), Bot(nombre="creador_webs"), Bot(nombre="chat_captacion")])
        session.commit()

@app.get("/health")
def health(session: Session = Depends(db)):
    session.execute(select(1))
    return {"ok": True, "database": "postgresql", "service": "negocio-automatico-api"}

@app.get("/leads/", response_model=dict)
def listar_leads(limit: int = Query(50, ge=1, le=200), session: Session = Depends(db)):
    rows = list(session.scalars(select(Lead).order_by(Lead.created_at.desc()).limit(limit)))
    return {"total": len(rows), "leads": [LeadOut.model_validate(row) for row in rows]}

@app.post("/leads/", response_model=LeadOut, status_code=201)
def crear_lead(payload: LeadIn, session: Session = Depends(db)):
    row = Lead(**payload.model_dump())
    session.add(row); session.commit(); session.refresh(row)
    return row

@app.get("/webs/", response_model=dict)
def listar_webs(session: Session = Depends(db)):
    rows = list(session.scalars(select(Website).order_by(Website.created_at.desc())))
    return {"total": len(rows), "webs": [WebsiteOut.model_validate(row) for row in rows]}

@app.post("/webs/", response_model=WebsiteOut, status_code=201)
def crear_web(payload: WebsiteIn, session: Session = Depends(db)):
    if session.scalar(select(Website).where(Website.dominio == payload.dominio)):
        raise HTTPException(409, "El dominio ya existe")
    row = Website(**payload.model_dump()); session.add(row); session.commit(); session.refresh(row)
    return row

@app.post("/pagos/nuevo", status_code=201)
def nuevo_pago(payload: PaymentIn, session: Session = Depends(db)):
    row = Payment(**payload.model_dump()); session.add(row); session.commit(); session.refresh(row)
    return {"ok": True, "pago": row.__dict__ | {"created_at": row.created_at.isoformat()}}

@app.get("/pagos/")
def listar_pagos(session: Session = Depends(db)):
    rows = list(session.scalars(select(Payment).order_by(Payment.created_at.desc())))
    return {"total": len(rows), "pagos": [r.__dict__ | {"created_at": r.created_at.isoformat()} for r in rows]}

@app.post("/retiros/nuevo", status_code=201)
def nuevo_retiro(payload: WithdrawalIn, session: Session = Depends(db)):
    row = Withdrawal(**payload.model_dump()); session.add(row); session.commit(); session.refresh(row)
    return {"ok": True, "retiro": row.__dict__ | {"created_at": row.created_at.isoformat()}}

@app.get("/retiros/")
def listar_retiros(session: Session = Depends(db)):
    rows = list(session.scalars(select(Withdrawal).order_by(Withdrawal.created_at.desc())))
    return {"total": len(rows), "retiros": [r.__dict__ | {"created_at": r.created_at.isoformat()} for r in rows]}

@app.get("/bots/")
def listar_bots(session: Session = Depends(db)):
    seed_bots(session); return {"total": session.scalar(select(func.count(Bot.id))), "bots": [b.__dict__ for b in session.scalars(select(Bot)).all()]}

def cambiar_bot(nombre: str, activo: bool, session: Session):
    seed_bots(session); bot = session.scalar(select(Bot).where(Bot.nombre == nombre))
    if not bot: raise HTTPException(404, "Bot no encontrado")
    bot.activo = activo; session.commit(); session.refresh(bot); return {"ok": True, "bot": bot.__dict__}

@app.post("/bots/activar")
def activar_bot(nombre: str, session: Session = Depends(db)): return cambiar_bot(nombre, True, session)
@app.post("/bots/desactivar")
def desactivar_bot(nombre: str, session: Session = Depends(db)): return cambiar_bot(nombre, False, session)

@app.get("/metricas/")
def ver_metricas(session: Session = Depends(db)):
    seed_bots(session)
    return {"leads_hoy": session.scalar(select(func.count(Lead.id))), "webs_hoy": session.scalar(select(func.count(Website.id))), "bots_activos": session.scalar(select(func.count(Bot.id)).where(Bot.activo.is_(True))), "retiros_realizados": session.scalar(select(func.count(Withdrawal.id)).where(Withdrawal.estado == "realizado"))}

@app.post("/usuarios/nuevo", status_code=201)
def nuevo_usuario(payload: UserIn, session: Session = Depends(db)):
    if session.scalar(select(User).where(User.email == str(payload.email))): raise HTTPException(409, "El email ya existe")
    row = User(nombre=payload.nombre, email=str(payload.email)); session.add(row); session.commit(); session.refresh(row)
    return {"ok": True, "usuario": {"id": row.id, "nombre": row.nombre, "email": row.email}}

@app.get("/usuarios/")
def listar_usuarios(session: Session = Depends(db)):
    rows = list(session.scalars(select(User).order_by(User.created_at.desc())))
    return {"total": len(rows), "usuarios": [{"id": r.id, "nombre": r.nombre, "email": r.email, "created_at": r.created_at.isoformat()} for r in rows]}

@app.get("/cerebros/")
def estado_cerebros():
    return {"leads": "activo", "webs": "activo", "pagos": "activo", "bots": "activo"}
