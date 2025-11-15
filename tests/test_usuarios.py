import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session
from datetime import date

client = TestClient(app)

# Limpiar base de datos antes de cada test
@pytest.fixture(autouse=True)
def setup_database():
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)
	yield


def test_create_usuario_exitoso():
	"""Test crear usuario con datos válidos"""
	usuario_data = {
		"nombre": "Juan",
		"apellido": "Pérez",
		"correo": "juan@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1995-05-15",
		"direccion": "Calle 123",
		"telefono": "3001234567",
		"acepta_terminos": True,
		"preferencias": ["Ficción", "Ciencia"]
	}
	
	response = client.post("/usuarios/", json=usuario_data)
	assert response.status_code == 201
	data = response.json()
	assert data["nombre"] == "Juan"
	assert data["correo"] == "juan@example.com"
	assert "contraseña" not in data  # No debe devolver la contraseña
	assert data["activo"] == False  # Inactivo hasta verificar email
	assert data["email_verificado"] == False  # Email no verificado inicialmente


def test_create_usuario_menor_edad():
	"""Test que no se puede crear usuario menor de 18 años"""
	usuario_data = {
		"nombre": "Carlos",
		"apellido": "López",
		"correo": "carlos@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "2015-01-01",  # Menor de 18
		"direccion": "Calle 456",
		"telefono": "3009876543",
		"acepta_terminos": True
	}
	
	response = client.post("/usuarios/", json=usuario_data)
	assert response.status_code == 400
	assert "18 años" in response.json()["detail"]


def test_create_usuario_sin_aceptar_terminos():
	"""Test que no se puede crear usuario sin aceptar términos"""
	usuario_data = {
		"nombre": "Ana",
		"apellido": "Gómez",
		"correo": "ana@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1990-03-20",
		"direccion": "Calle 789",
		"telefono": "3005555555",
		"acepta_terminos": False
	}
	
	response = client.post("/usuarios/", json=usuario_data)
	assert response.status_code == 400
	assert "términos" in response.json()["detail"]


def test_create_usuario_correo_duplicado():
	"""Test que no se puede crear usuario con correo duplicado"""
	usuario_data = {
		"nombre": "Pedro",
		"apellido": "Martínez",
		"correo": "pedro@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1988-07-10",
		"direccion": "Calle 321",
		"telefono": "3007777777",
		"acepta_terminos": True
	}
	
	# Primer usuario
	response = client.post("/usuarios/", json=usuario_data)
	assert response.status_code == 201
	
	# Segundo usuario con mismo correo
	response = client.post("/usuarios/", json=usuario_data)
	assert response.status_code == 400
	assert "correo ya existe" in response.json()["detail"]


def test_get_usuario_por_id():
	"""Test obtener usuario por ID"""
	# Crear usuario
	usuario_data = {
		"nombre": "María",
		"apellido": "Rodríguez",
		"correo": "maria@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1992-11-25",
		"direccion": "Calle 555",
		"telefono": "3008888888",
		"acepta_terminos": True
	}
	create_response = client.post("/usuarios/", json=usuario_data)
	usuario_id = create_response.json()["idusuario"]
	
	# Obtener usuario
	response = client.get(f"/usuarios/{usuario_id}")
	assert response.status_code == 200
	data = response.json()
	assert data["nombre"] == "María"
	assert data["correo"] == "maria@example.com"


def test_get_usuario_no_existente():
	"""Test obtener usuario que no existe"""
	response = client.get("/usuarios/9999")
	assert response.status_code == 404


def test_update_usuario():
	"""Test actualizar datos de usuario"""
	# Crear usuario
	usuario_data = {
		"nombre": "Luis",
		"apellido": "Hernández",
		"correo": "luis@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1985-04-15",
		"direccion": "Calle 666",
		"telefono": "3009999999",
		"acepta_terminos": True
	}
	create_response = client.post("/usuarios/", json=usuario_data)
	usuario_id = create_response.json()["idusuario"]
	
	# Actualizar usuario
	update_data = {
		"nombre": "Luis Alberto",
		"direccion": "Nueva Calle 777"
	}
	response = client.put(f"/usuarios/{usuario_id}", json=update_data)
	assert response.status_code == 200
	data = response.json()
	assert data["nombre"] == "Luis Alberto"
	assert data["direccion"] == "Nueva Calle 777"


def test_delete_usuario():
	"""Test eliminar usuario"""
	# Crear usuario
	usuario_data = {
		"nombre": "Sofia",
		"apellido": "Torres",
		"correo": "sofia@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1998-09-30",
		"direccion": "Calle 888",
		"telefono": "3001111111",
		"acepta_terminos": True
	}
	create_response = client.post("/usuarios/", json=usuario_data)
	usuario_id = create_response.json()["idusuario"]
	
	# Eliminar usuario
	response = client.delete(f"/usuarios/{usuario_id}")
	assert response.status_code == 204
	
	# Verificar que ya no existe
	response = client.get(f"/usuarios/{usuario_id}")
	assert response.status_code == 404


def test_listar_usuarios():
	"""Test listar todos los usuarios"""
	# Crear varios usuarios
	for i in range(3):
		usuario_data = {
			"nombre": f"Usuario{i}",
			"apellido": f"Apellido{i}",
			"correo": f"usuario{i}@example.com",
			"contraseña": "password123",
			"rol": "CLIENTE",
			"fecha_nacimiento": "1990-01-01",
			"direccion": f"Calle {i}",
			"telefono": f"300000000{i}",
			"acepta_terminos": True
		}
		client.post("/usuarios/", json=usuario_data)
	
	# Listar usuarios
	response = client.get("/usuarios/")
	assert response.status_code == 200
	data = response.json()
	assert len(data) == 3
