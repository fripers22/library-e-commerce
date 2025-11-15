from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.inventario_service import InventarioService
from app.domain.inventario_model import InventarioCreate, InventarioUpdate, InventarioReabastecer, InventarioResponse

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.post("/", response_model=InventarioResponse, status_code=201)
def create_inventario(inventario_data: InventarioCreate, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.create_inventario(inventario_data)


@router.get("/{inventario_id}", response_model=InventarioResponse)
def get_inventario(inventario_id: int, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.get_inventario(inventario_id)


@router.get("/libro/{idlibro}", response_model=InventarioResponse)
def get_inventario_by_book(idlibro: int, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.get_inventario_by_book(idlibro)


@router.get("/bajo-stock/", response_model=list[InventarioResponse])
def get_inventarios_bajo_stock(db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.get_inventarios_bajo_stock()


@router.post("/{inventario_id}/reabastecer", response_model=InventarioResponse)
def reabastecer_inventario(inventario_id: int, reabastecer_data: InventarioReabastecer, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.reabastecer(inventario_id, reabastecer_data)


@router.post("/{inventario_id}/reservar/{cantidad}", response_model=InventarioResponse)
def reservar_stock(inventario_id: int, cantidad: int, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.reservar_stock(inventario_id, cantidad)


@router.post("/{inventario_id}/liberar/{cantidad}", response_model=InventarioResponse)
def liberar_stock(inventario_id: int, cantidad: int, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.liberar_stock(inventario_id, cantidad)


@router.put("/{inventario_id}", response_model=InventarioResponse)
def update_inventario(inventario_id: int, inventario_data: InventarioUpdate, db: Session = Depends(get_db)):
	service = InventarioService(db)
	return service.update_inventario(inventario_id, inventario_data)


@router.delete("/{inventario_id}", status_code=204)
def delete_inventario(inventario_id: int, db: Session = Depends(get_db)):
	service = InventarioService(db)
	service.delete_inventario(inventario_id)
	return None
