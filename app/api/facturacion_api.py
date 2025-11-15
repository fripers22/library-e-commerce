from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.facturacion_service import FacturacionService
from app.domain.facturacion_model import FacturacionCreate, FacturacionUpdate, FacturacionResponse
from pydantic import BaseModel

router = APIRouter(prefix="/facturacion", tags=["Facturación"])


class CreateFacturaFromPedido(BaseModel):
	pedido_id: int


@router.post("/", response_model=FacturacionResponse, status_code=201)
def create_facturacion(facturacion_data: FacturacionCreate, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	return service.create_facturacion(facturacion_data)


@router.post("/from-pedido", response_model=FacturacionResponse, status_code=201)
def create_facturacion_from_pedido(data: CreateFacturaFromPedido, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	return service.create_facturacion_from_pedido(data.pedido_id)


@router.get("/{factura_id}", response_model=FacturacionResponse)
def get_facturacion(factura_id: int, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	return service.get_facturacion(factura_id)


@router.get("/usuario/{idusuario}", response_model=list[FacturacionResponse])
def get_facturaciones_by_user(idusuario: int, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	return service.get_facturaciones_by_user(idusuario)


@router.get("/pedido/{pedido_id}", response_model=FacturacionResponse)
def get_facturacion_by_pedido(pedido_id: int, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	return service.get_facturacion_by_pedido(pedido_id)


@router.put("/{factura_id}", response_model=FacturacionResponse)
def update_facturacion(factura_id: int, facturacion_data: FacturacionUpdate, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	return service.update_facturacion(factura_id, facturacion_data)


@router.delete("/{factura_id}", status_code=204)
def delete_facturacion(factura_id: int, db: Session = Depends(get_db)):
	service = FacturacionService(db)
	service.delete_facturacion(factura_id)
	return None
