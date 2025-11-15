from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.pedido_service import PedidoService
from app.domain.pedido_model import PedidoCreate, PedidoUpdate, PedidoResponse
from pydantic import BaseModel

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


class CreatePedidoFromCarrito(BaseModel):
	carrito_id: int
	metodo_pago: str
	direccion_envio: str


@router.post("/", response_model=PedidoResponse, status_code=201)
def create_pedido(pedido_data: PedidoCreate, db: Session = Depends(get_db)):
	service = PedidoService(db)
	return service.create_pedido(pedido_data)


@router.post("/from-carrito", response_model=PedidoResponse, status_code=201)
def create_pedido_from_carrito(data: CreatePedidoFromCarrito, db: Session = Depends(get_db)):
	service = PedidoService(db)
	return service.create_pedido_from_carrito(data.carrito_id, data.metodo_pago, data.direccion_envio)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
	service = PedidoService(db)
	return service.get_pedido(pedido_id)


@router.get("/usuario/{idusuario}", response_model=list[PedidoResponse])
def get_pedidos_by_user(idusuario: int, db: Session = Depends(get_db)):
	service = PedidoService(db)
	return service.get_pedidos_by_user(idusuario)


@router.put("/{pedido_id}", response_model=PedidoResponse)
def update_pedido(pedido_id: int, pedido_data: PedidoUpdate, db: Session = Depends(get_db)):
	service = PedidoService(db)
	return service.update_pedido(pedido_id, pedido_data)


@router.delete("/{pedido_id}", status_code=204)
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
	service = PedidoService(db)
	service.delete_pedido(pedido_id)
	return None
