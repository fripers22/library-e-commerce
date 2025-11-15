import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)
	yield


@pytest.fixture
def usuario_creado():
	"""Fixture para crear un usuario de prueba"""
	usuario_data = {
		"nombre": "Test",
		"apellido": "User",
		"correo": "test@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1990-01-01",
		"direccion": "Calle Test",
		"telefono": "3001234567",
		"acepta_terminos": True
	}
	response = client.post("/usuarios/", json=usuario_data)
	return response.json()["idusuario"]


@pytest.fixture
def libro_creado():
	"""Fixture para crear un libro de prueba"""
	libro_data = {
		"titulo": "Libro Test",
		"autor": ["Autor Test"],
		"categoria": ["Test"],
		"precio": "25000.00",
		"stock": 50,
		"año_publicacion": 2023,
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	response = client.post("/libros/", json=libro_data)
	return response.json()["idlibro"]


def test_create_carrito(usuario_creado):
	"""Test crear carrito para un usuario"""
	carrito_data = {
		"idusuario": usuario_creado,
		"sesion_id": "session123"
	}
	
	response = client.post("/carritos/", json=carrito_data)
	assert response.status_code == 201
	data = response.json()
	assert data["idusuario"] == usuario_creado
	assert data["total"] == "0"


def test_add_item_to_carrito(usuario_creado, libro_creado):
	"""Test agregar item al carrito"""
	# Crear carrito
	carrito_data = {
		"idusuario": usuario_creado
	}
	carrito_response = client.post("/carritos/", json=carrito_data)
	carrito_id = carrito_response.json()["idcarrito"]
	
	# Agregar item
	item_data = {
		"idlibro": libro_creado,
		"cantidad": 2
	}
	response = client.post(f"/carritos/{carrito_id}/items", json=item_data)
	assert response.status_code == 200
	data = response.json()
	assert len(data["items"]) == 1
	assert float(data["total"]) > 0


def test_add_item_stock_insuficiente(usuario_creado, libro_creado):
	"""Test que no se puede agregar más items del stock disponible"""
	# Crear carrito
	carrito_data = {
		"idusuario": usuario_creado
	}
	carrito_response = client.post("/carritos/", json=carrito_data)
	carrito_id = carrito_response.json()["idcarrito"]
	
	# Intentar agregar más items del stock
	item_data = {
		"idlibro": libro_creado,
		"cantidad": 1000
	}
	response = client.post(f"/carritos/{carrito_id}/items", json=item_data)
	assert response.status_code == 400
	assert "stock" in response.json()["detail"].lower()


def test_remove_item_from_carrito(usuario_creado, libro_creado):
	"""Test eliminar item del carrito"""
	# Crear carrito y agregar item
	carrito_data = {
		"idusuario": usuario_creado
	}
	carrito_response = client.post("/carritos/", json=carrito_data)
	carrito_id = carrito_response.json()["idcarrito"]
	
	item_data = {
		"idlibro": libro_creado,
		"cantidad": 2
	}
	client.post(f"/carritos/{carrito_id}/items", json=item_data)
	
	# Eliminar item
	response = client.delete(f"/carritos/{carrito_id}/items/{libro_creado}")
	assert response.status_code == 200
	data = response.json()
	assert len(data["items"]) == 0


def test_get_carrito_by_user(usuario_creado):
	"""Test obtener carrito por usuario"""
	# Crear carrito
	carrito_data = {
		"idusuario": usuario_creado
	}
	client.post("/carritos/", json=carrito_data)
	
	# Obtener carrito
	response = client.get(f"/carritos/usuario/{usuario_creado}")
	assert response.status_code == 200
	data = response.json()
	assert data["idusuario"] == usuario_creado


def test_calcular_totales_con_iva(usuario_creado, libro_creado):
	"""Test que el carrito calcula IVA correctamente (19%)"""
	# Crear carrito
	carrito_data = {
		"idusuario": usuario_creado
	}
	carrito_response = client.post("/carritos/", json=carrito_data)
	carrito_id = carrito_response.json()["idcarrito"]
	
	# Agregar item
	item_data = {
		"idlibro": libro_creado,
		"cantidad": 1
	}
	response = client.post(f"/carritos/{carrito_id}/items", json=item_data)
	data = response.json()
	
	# Verificar que hay IVA (19%)
	subtotal = float(data["subtotal"])
	impuestos = float(data["impuestos"])
	total = float(data["total"])
	
	assert impuestos > 0
	assert abs(impuestos - (subtotal * 0.19)) < 0.01  # IVA del 19%
	assert abs(total - (subtotal + impuestos)) < 0.01
