from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.user_service import UserService
from app.domain.user_model import UserCreate, UserUpdate, UserResponse
from pydantic import BaseModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_db():
	"""Yield a database session and ensure it's closed."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
	"""Create a new user."""
	service = UserService(db)
	return service.create_user(user)


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
	"""Get all users."""
	service = UserService(db)
	return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
	"""Get a user by ID."""
	service = UserService(db)
	return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
	"""Update a user."""
	service = UserService(db)
	return service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
	"""Delete a user."""
	service = UserService(db)
	service.delete_user(user_id)
	return None


class VerifyEmailResponse(BaseModel):
	message: str
	email_verificado: bool


@router.post('/verificar/{token}', response_model=VerifyEmailResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
	service = UserService(db)
	user = service.repository.get_user_by_token(token)
	if not user:
		raise HTTPException(status_code=404, detail='Token invalido')
	if user.email_verificado:
		return VerifyEmailResponse(message='Ya verificado', email_verificado=True)
	service.repository.verify_email(user)
	return VerifyEmailResponse(message=f'Correo {user.correo} verificado', email_verificado=True)


@router.post('/enviar-verificacion/{user_id}', response_model=dict)
def send_verification_email(user_id: int, db: Session = Depends(get_db)):
	service = UserService(db)
	user = service.get_user(user_id)
	if user.email_verificado:
		raise HTTPException(status_code=400, detail='Ya verificado')
	user_db = service.repository.get_user_by_id(user_id)
	return {
		'message': f'Email enviado a {user.correo}',
		'token': user_db.token_verificacion,
		'verificacion_url': f'/usuarios/verificar/{user_db.token_verificacion}'
	}
