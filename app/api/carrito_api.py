from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.carrito_service import CarritoService
from app.domain.carrito_model import CarritoCreate, CarritoAddItem, CarritoUpdate, CarritoResponse

router = APIRouter(prefix="/carritos", tags=["Carritos"])


@router.post("/", response_model=CarritoResponse, status_code=201)
def create_carrito(carrito_data: CarritoCreate, db: Session = Depends(get_db)):
	service = CarritoService(db)
	return service.create_carrito(carrito_data)


@router.get("/{carrito_id}", response_model=CarritoResponse)
def get_carrito(carrito_id: int, db: Session = Depends(get_db)):
	service = CarritoService(db)
	return service.get_carrito(carrito_id)


@router.get("/usuario/{idusuario}", response_model=CarritoResponse)
def get_carrito_by_user(idusuario: int, db: Session = Depends(get_db)):
	service = CarritoService(db)
	return service.get_carrito_by_user(idusuario)


@router.post("/{carrito_id}/items", response_model=CarritoResponse)
def add_item_to_carrito(carrito_id: int, item_data: CarritoAddItem, db: Session = Depends(get_db)):
	service = CarritoService(db)
	return service.add_item(carrito_id, item_data)


@router.delete("/{carrito_id}/items/{idlibro}", response_model=CarritoResponse)
def remove_item_from_carrito(carrito_id: int, idlibro: int, db: Session = Depends(get_db)):
	service = CarritoService(db)
	return service.remove_item(carrito_id, idlibro)


@router.put("/{carrito_id}", response_model=CarritoResponse)
def update_carrito(carrito_id: int, carrito_data: CarritoUpdate, db: Session = Depends(get_db)):
	service = CarritoService(db)
	return service.update_carrito(carrito_id, carrito_data)


@router.delete("/{carrito_id}", status_code=204)
def delete_carrito(carrito_id: int, db: Session = Depends(get_db)):
	service = CarritoService(db)
	service.delete_carrito(carrito_id)
	return None
