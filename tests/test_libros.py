import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from datetime import datetime

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)
	yield


def test_create_libro_exitoso():
	"""Test crear libro con datos válidos"""
	libro_data = {
		"titulo": "Cien Años de Soledad",
		"autor": ["Gabriel García Márquez"],
		"categoria": ["Ficción", "Realismo Mágico"],
		"precio": "45000.00",
		"stock": 10,
		"editorial": "Editorial Sudamericana",
		"año_publicacion": 1967,
		"idioma": "Español",
		"formato": "Tapa Dura",
		"descripcion": "Una obra maestra de la literatura",
		"descuento": "0.00"
	}
	
	response = client.post("/libros/", json=libro_data)
	assert response.status_code == 201
	data = response.json()
	assert data["titulo"] == "Cien Años de Soledad"
	assert data["precio"] == "45000.00"
	assert data["stock"] == 10


def test_create_libro_año_invalido():
	"""Test que no se puede crear libro con año anterior a 1700"""
	libro_data = {
		"titulo": "Libro Antiguo",
		"autor": ["Autor Desconocido"],
		"categoria": ["Historia"],
		"precio": "20000.00",
		"stock": 5,
		"año_publicacion": 1500,  # Anterior a 1700
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	
	response = client.post("/libros/", json=libro_data)
	assert response.status_code == 400
	assert "1700" in response.json()["detail"]


def test_create_libro_año_futuro():
	"""Test que no se puede crear libro con año futuro"""
	año_futuro = datetime.now().year + 10
	libro_data = {
		"titulo": "Libro del Futuro",
		"autor": ["Autor Futurista"],
		"categoria": ["Ciencia Ficción"],
		"precio": "30000.00",
		"stock": 5,
		"año_publicacion": año_futuro,
		"idioma": "Español",
		"formato": "E-book"
	}
	
	response = client.post("/libros/", json=libro_data)
	assert response.status_code == 400


def test_create_libro_precio_negativo():
	"""Test que no se puede crear libro con precio negativo"""
	libro_data = {
		"titulo": "Libro Gratis",
		"autor": ["Autor Generoso"],
		"categoria": ["Educación"],
		"precio": "-10000.00",
		"stock": 5,
		"año_publicacion": 2020,
		"idioma": "Español",
		"formato": "E-book"
	}
	
	response = client.post("/libros/", json=libro_data)
	assert response.status_code == 400
	assert "precio" in response.json()["detail"].lower()


def test_create_libro_stock_negativo():
	"""Test que no se puede crear libro con stock negativo"""
	libro_data = {
		"titulo": "Libro Sin Stock",
		"autor": ["Autor"],
		"categoria": ["General"],
		"precio": "25000.00",
		"stock": -5,
		"año_publicacion": 2021,
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	
	response = client.post("/libros/", json=libro_data)
	assert response.status_code == 400
	assert "stock" in response.json()["detail"].lower()


def test_get_libro_por_id():
	"""Test obtener libro por ID"""
	# Crear libro
	libro_data = {
		"titulo": "El Principito",
		"autor": ["Antoine de Saint-Exupéry"],
		"categoria": ["Infantil"],
		"precio": "18000.00",
		"stock": 20,
		"año_publicacion": 1943,
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	create_response = client.post("/libros/", json=libro_data)
	libro_id = create_response.json()["idlibro"]
	
	# Obtener libro
	response = client.get(f"/libros/{libro_id}")
	assert response.status_code == 200
	data = response.json()
	assert data["titulo"] == "El Principito"


def test_update_libro():
	"""Test actualizar datos de libro"""
	# Crear libro
	libro_data = {
		"titulo": "1984",
		"autor": ["George Orwell"],
		"categoria": ["Distopía"],
		"precio": "35000.00",
		"stock": 15,
		"año_publicacion": 1949,
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	create_response = client.post("/libros/", json=libro_data)
	libro_id = create_response.json()["idlibro"]
	
	# Actualizar libro
	update_data = {
		"precio": "32000.00",
		"stock": 25,
		"descuento": "10.00"
	}
	response = client.put(f"/libros/{libro_id}", json=update_data)
	assert response.status_code == 200
	data = response.json()
	assert data["precio"] == "32000.00"
	assert data["stock"] == 25
	assert data["descuento"] == "10.00"


def test_delete_libro():
	"""Test eliminar libro"""
	# Crear libro
	libro_data = {
		"titulo": "Libro Temporal",
		"autor": ["Autor Temporal"],
		"categoria": ["Varios"],
		"precio": "15000.00",
		"stock": 5,
		"año_publicacion": 2023,
		"idioma": "Español",
		"formato": "E-book"
	}
	create_response = client.post("/libros/", json=libro_data)
	libro_id = create_response.json()["idlibro"]
	
	# Eliminar libro
	response = client.delete(f"/libros/{libro_id}")
	assert response.status_code == 204
	
	# Verificar que ya no existe
	response = client.get(f"/libros/{libro_id}")
	assert response.status_code == 404


def test_listar_libros():
	"""Test listar todos los libros"""
	# Crear varios libros
	for i in range(3):
		libro_data = {
			"titulo": f"Libro {i}",
			"autor": [f"Autor {i}"],
			"categoria": ["General"],
			"precio": f"{20000 + i * 5000}.00",
			"stock": 10 + i,
			"año_publicacion": 2020 + i,
			"idioma": "Español",
			"formato": "Tapa Dura"
		}
		client.post("/libros/", json=libro_data)
	
	# Listar libros
	response = client.get("/libros/")
	assert response.status_code == 200
	data = response.json()
	assert len(data) == 3
