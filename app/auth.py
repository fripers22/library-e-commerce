from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.repository.user_repository import UserRepository
import bcrypt

# Configuración JWT
SECRET_KEY = "tu_clave_secreta_super_segura_cambiala_en_produccion"  # ⚠️ Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	"""Crea un token JWT"""
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""Verifica la contraseña hasheada"""
	password_bytes = plain_password.encode('utf-8')[:72]
	hashed_bytes = hashed_password.encode('utf-8')
	return bcrypt.checkpw(password_bytes, hashed_bytes)


def authenticate_user(db: Session, correo: str, contraseña: str):
	"""Autentica un usuario verificando correo y contraseña"""
	user_repo = UserRepository(db)
	user = user_repo.get_user_by_email(correo)
	
	if not user:
		return None
	
	if not verify_password(contraseña, user.contraseña):
		return None
	
	return user


def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db)
):
	"""Obtiene el usuario actual desde el token JWT"""
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="No se pudo validar las credenciales",
		headers={"WWW-Authenticate": "Bearer"},
	)
	
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		user_id: int = payload.get("sub")
		if user_id is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	
	user_repo = UserRepository(db)
	user = user_repo.get_user_by_id(user_id)
	
	if user is None:
		raise credentials_exception
	
	return user


def require_role(allowed_roles: list[str]):
	"""Decorator para verificar que el usuario tenga uno de los roles permitidos"""
	def role_checker(current_user = Depends(get_current_user)):
		if current_user.rol not in allowed_roles:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail=f"No tienes permisos. Se requiere rol: {', '.join(allowed_roles)}"
			)
		return current_user
	return role_checker
