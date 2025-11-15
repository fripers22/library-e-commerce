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


def test_flujo_compra_completo():
	"""Test del flujo completo: Usuario → Libro → Carrito → Pedido → Factura"""
	
	# 1. Crear usuario
	usuario_data = {
		"nombre": "Cliente",
		"apellido": "Prueba",
		"correo": "cliente@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1990-01-01",
		"direccion": "Calle Principal 123",
		"telefono": "3001234567",
		"acepta_terminos": True
	}
	usuario_response = client.post("/usuarios/", json=usuario_data)
	assert usuario_response.status_code == 201
	idusuario = usuario_response.json()["idusuario"]
	
	# 2. Crear libro
	libro_data = {
		"titulo": "Cien Años de Soledad",
		"autor": ["Gabriel García Márquez"],
		"categoria": ["Clásicos", "Literatura Latinoamericana"],
		"precio": "50000.00",
		"stock": 100,
		"año_publicacion": 1967,
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	libro_response = client.post("/libros/", json=libro_data)
	assert libro_response.status_code == 201
	idlibro = libro_response.json()["idlibro"]
	stock_inicial = libro_response.json()["stock"]
	
	# 3. Crear inventario para el libro
	inventario_data = {
		"idlibro": idlibro,
		"stock_disponible": 100,
		"stock_reservado": 0,
		"umbral_minimo": 10,
		"ubicacion_almacen": "Almacén A"
	}
	inventario_response = client.post("/inventario/", json=inventario_data)
	assert inventario_response.status_code == 201
	
	# 4. Crear carrito
	carrito_data = {
		"idusuario": idusuario
	}
	carrito_response = client.post("/carritos/", json=carrito_data)
	assert carrito_response.status_code == 201
	idcarrito = carrito_response.json()["idcarrito"]
	
	# 5. Agregar libro al carrito
	item_data = {
		"idlibro": idlibro,
		"cantidad": 3
	}
	add_item_response = client.post(f"/carritos/{idcarrito}/items", json=item_data)
	assert add_item_response.status_code == 200
	carrito_actualizado = add_item_response.json()
	
	# Verificar totales del carrito
	assert len(carrito_actualizado["items"]) == 1
	assert float(carrito_actualizado["subtotal"]) == 150000.00
	assert float(carrito_actualizado["impuestos"]) == 28500.00  # 19% IVA
	assert float(carrito_actualizado["total"]) == 178500.00
	
	# 6. Crear pedido desde el carrito
	pedido_data = {
		"carrito_id": idcarrito,
		"metodo_pago": "TARJETA",
		"direccion_envio": "Calle Principal 123"
	}
	pedido_response = client.post("/pedidos/from-carrito", json=pedido_data)
	assert pedido_response.status_code == 201
	pedido = pedido_response.json()
	idpedido = pedido["idpedido"]
	
	# Verificar pedido
	assert pedido["estado"] == "PENDIENTE"
	assert pedido["idusuario"] == idusuario
	assert len(pedido["items"]) == 1
	assert float(pedido["total"]) == 178500.00
	
	# 7. Verificar que el stock se redujo
	libro_actualizado = client.get(f"/libros/{idlibro}")
	assert libro_actualizado.status_code == 200
	assert libro_actualizado.json()["stock"] == stock_inicial - 3
	
	# 8. Generar factura desde el pedido
	factura_data = {
		"pedido_id": idpedido
	}
	factura_response = client.post("/facturacion/from-pedido", json=factura_data)
	assert factura_response.status_code == 201
	factura = factura_response.json()
	
	# Verificar factura
	assert factura["idpedido"] == idpedido
	assert factura["idusuario"] == idusuario
	assert factura["estado"] == "EMITIDA"
	assert float(factura["total"]) == 178500.00
	assert float(factura["impuesto"]) == 28500.00
	
	# 9. Verificar que el carrito cambió a CONVERTIDO
	carrito_final = client.get(f"/carritos/{idcarrito}")
	assert carrito_final.status_code == 200
	assert carrito_final.json()["estado"] == "CONVERTIDO"
	
	# 10. Verificar inventario actualizado
	inventario_final = client.get(f"/inventario/libro/{idlibro}")
	assert inventario_final.status_code == 200
	assert inventario_final.json()["stock_disponible"] == 97  # 100 - 3
	
	print("✅ Flujo completo exitoso: Usuario → Carrito → Pedido → Factura")


def test_flujo_multiples_libros():
	"""Test de compra con múltiples libros"""
	
	# Crear usuario
	usuario_data = {
		"nombre": "Comprador",
		"apellido": "Multiple",
		"correo": "multiple@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1985-05-15",
		"direccion": "Avenida 456",
		"telefono": "3009876543",
		"acepta_terminos": True
	}
	usuario_response = client.post("/usuarios/", json=usuario_data)
	idusuario = usuario_response.json()["idusuario"]
	
	# Crear varios libros
	libros_ids = []
	for i in range(3):
		libro_data = {
			"titulo": f"Libro {i+1}",
			"autor": [f"Autor {i+1}"],
			"categoria": ["General"],
			"precio": f"{(i+1) * 10000}.00",
			"stock": 50,
			"año_publicacion": 2020 + i,
			"idioma": "Español",
			"formato": "Tapa Dura"
		}
		libro_response = client.post("/libros/", json=libro_data)
		idlibro = libro_response.json()["idlibro"]
		libros_ids.append(idlibro)
		
		# Crear inventario
		inventario_data = {
			"idlibro": idlibro,
			"stock_disponible": 50,
			"umbral_minimo": 5,
			"ubicacion_almacen": f"Estante {i+1}"
		}
		client.post("/inventario/", json=inventario_data)
	
	# Crear carrito
	carrito_data = {"idusuario": idusuario}
	carrito_response = client.post("/carritos/", json=carrito_data)
	idcarrito = carrito_response.json()["idcarrito"]
	
	# Agregar todos los libros al carrito
	for idlibro in libros_ids:
		item_data = {
			"idlibro": idlibro,
			"cantidad": 2
		}
		client.post(f"/carritos/{idcarrito}/items", json=item_data)
	
	# Verificar carrito tiene 3 items
	carrito = client.get(f"/carritos/{idcarrito}").json()
	assert len(carrito["items"]) == 3
	
	# Crear pedido
	pedido_data = {
		"carrito_id": idcarrito,
		"metodo_pago": "PAYPAL",
		"direccion_envio": "Avenida 456"
	}
	pedido_response = client.post("/pedidos/from-carrito", json=pedido_data)
	assert pedido_response.status_code == 201
	assert len(pedido_response.json()["items"]) == 3


def test_flujo_stock_insuficiente():
	"""Test que falla cuando no hay suficiente stock"""
	
	# Crear usuario
	usuario_data = {
		"nombre": "Usuario",
		"apellido": "Stock",
		"correo": "stock@example.com",
		"contraseña": "password123",
		"rol": "CLIENTE",
		"fecha_nacimiento": "1992-03-20",
		"direccion": "Calle Stock",
		"telefono": "3005555555",
		"acepta_terminos": True
	}
	usuario_response = client.post("/usuarios/", json=usuario_data)
	idusuario = usuario_response.json()["idusuario"]
	
	# Crear libro con stock limitado
	libro_data = {
		"titulo": "Libro Limitado",
		"autor": ["Autor"],
		"categoria": ["Test"],
		"precio": "20000.00",
		"stock": 5,
		"año_publicacion": 2023,
		"idioma": "Español",
		"formato": "Tapa Dura"
	}
	libro_response = client.post("/libros/", json=libro_data)
	idlibro = libro_response.json()["idlibro"]
	
	# Crear carrito
	carrito_data = {"idusuario": idusuario}
	carrito_response = client.post("/carritos/", json=carrito_data)
	idcarrito = carrito_response.json()["idcarrito"]
	
	# Intentar agregar más del stock disponible
	item_data = {
		"idlibro": idlibro,
		"cantidad": 10
	}
	response = client.post(f"/carritos/{idcarrito}/items", json=item_data)
	assert response.status_code == 400
	assert "stock" in response.json()["detail"].lower()
