from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from app.database import get_db
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class Token(BaseModel):
	access_token: str
	token_type: str


class LoginResponse(BaseModel):
	access_token: str
	token_type: str
	idusuario: int
	nombre: str
	correo: str
	rol: str


@router.post("/login", response_model=LoginResponse)
def login(
	form_data: OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db)
):
	"""
	Endpoint de autenticación (Login)
	- username: correo electrónico del usuario
	- password: contraseña
	"""
	user = authenticate_user(db, form_data.username, form_data.password)
	
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Correo o contraseña incorrectos",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	# Crear token JWT
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.idusuario, "rol": user.rol},
		expires_delta=access_token_expires
	)
	
	return LoginResponse(
		access_token=access_token,
		token_type="bearer",
		idusuario=user.idusuario,
		nombre=user.nombre,
		correo=user.correo,
		rol=user.rol
	)
