"""
Script para insertar datos de prueba en la base de datos
Ejecutar con: python scripts/seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, Base, engine
from app.repository.user_repository import UserRepository
from app.repository.book_repository import BookRepository
from app.repository.inventario_repository import InventarioRepository
from app.repository.carrito_repository import CarritoRepository
from app.repository.pedido_repository import PedidoRepository
from app.repository.facturacion_repository import FacturacionRepository
from datetime import date, datetime
from decimal import Decimal

def seed_users(db):
	"""Crear usuarios de prueba"""
	print("📝 Creando usuarios...")
	user_repo = UserRepository(db)
	
	users_data = [
		{
			"nombre": "Admin",
			"apellido": "Sistema",
			"correo": "admin@libreria.com",
			"contraseña": "admin123",
			"rol": "ADMIN",
			"fecha_nacimiento": date(1990, 1, 1),
			"direccion": "Calle Admin 123",
			"telefono": "3001234567",
			"preferencias": ["Administración", "Gestión"],
			"acepta_terminos": True
		},
		{
			"nombre": "Cliente",
			"apellido": "Demo",
			"correo": "cliente@example.com",
			"contraseña": "cliente123",
			"rol": "CLIENTE",
			"fecha_nacimiento": date(1995, 5, 15),
			"direccion": "Avenida Principal 456",
			"telefono": "3009876543",
			"preferencias": ["Ficción", "Ciencia", "Historia"],
			"acepta_terminos": True
		},
		{
			"nombre": "Vendedor",
			"apellido": "Pro",
			"correo": "vendedor@libreria.com",
			"contraseña": "vendedor123",
			"rol": "VENDEDOR",
			"fecha_nacimiento": date(1988, 10, 20),
			"direccion": "Calle Comercio 789",
			"telefono": "3005555555",
			"preferencias": ["Ventas", "Marketing"],
			"acepta_terminos": True
		}
	]
	
	created_users = []
	for user_data in users_data:
		# Verificar si ya existe
		existing = user_repo.get_user_by_email(user_data["correo"])
		if existing:
			print(f"   ⚠️  Usuario {user_data['correo']} ya existe, omitiendo...")
			created_users.append(existing)
			continue
		
		user = user_repo.create_user(**user_data)
		# Activar y verificar email automáticamente para usuarios de prueba
		user.email_verificado = True
		user.activo = True
		db.commit()
		print(f"   ✅ Usuario creado: {user.correo} (Rol: {user.rol})")
		created_users.append(user)
	
	return created_users


def seed_books(db):
	"""Crear libros de prueba"""
	print("\n📚 Creando libros...")
	book_repo = BookRepository(db)
	
	books_data = [
		{
			"titulo": "Cien Años de Soledad",
			"autor": ["Gabriel García Márquez"],
			"categoria": ["Clásicos", "Literatura Latinoamericana"],
			"precio": "50000.00",
			"stock": 25,
			"editorial": "Editorial Sudamericana",
			"año_publicacion": 1967,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Obra maestra del realismo mágico"
		},
		{
			"titulo": "El Quijote",
			"autor": ["Miguel de Cervantes"],
			"categoria": ["Clásicos", "Aventuras"],
			"precio": "45000.00",
			"stock": 30,
			"editorial": "RAE",
			"año_publicacion": 1605,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Clásico de la literatura española"
		},
		{
			"titulo": "1984",
			"autor": ["George Orwell"],
			"categoria": ["Ciencia Ficción", "Distopía"],
			"precio": "38000.00",
			"stock": 40,
			"editorial": "Secker & Warburg",
			"año_publicacion": 1949,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Novela distópica sobre totalitarismo"
		},
		{
			"titulo": "El Principito",
			"autor": ["Antoine de Saint-Exupéry"],
			"categoria": ["Infantil", "Filosof\u00eda"],
			"precio": "25000.00",
			"stock": 50,
			"editorial": "Reynal & Hitchcock",
			"año_publicacion": 1943,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Cuento poético para niños y adultos"
		},
		{
			"titulo": "Harry Potter y la Piedra Filosofal",
			"autor": ["J.K. Rowling"],
			"categoria": ["Fantasía", "Juvenil"],
			"precio": "55000.00",
			"stock": 60,
			"editorial": "Bloomsbury",
			"año_publicacion": 1997,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Primera aventura del joven mago"
		},
		{
			"titulo": "Sapiens: De animales a dioses",
			"autor": ["Yuval Noah Harari"],
			"categoria": ["Historia", "Ciencia"],
			"precio": "62000.00",
			"stock": 35,
			"editorial": "Debate",
			"año_publicacion": 2011,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Historia de la humanidad"
		},
		{
			"titulo": "El Amor en los Tiempos del Cólera",
			"autor": ["Gabriel García Márquez"],
			"categoria": ["Romance", "Literatura Latinoamericana"],
			"precio": "48000.00",
			"stock": 28,
			"editorial": "Oveja Negra",
			"año_publicacion": 1985,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Historia de amor épica"
		},
		{
			"titulo": "Breve Historia del Tiempo",
			"autor": ["Stephen Hawking"],
			"categoria": ["Ciencia", "Física"],
			"precio": "42000.00",
			"stock": 22,
			"editorial": "Bantam Books",
			"año_publicacion": 1988,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Cosmología para el público general"
		},
		{
			"titulo": "Crónica de una Muerte Anunciada",
			"autor": ["Gabriel García Márquez"],
			"categoria": ["Clásicos", "Misterio"],
			"precio": "35000.00",
			"stock": 32,
			"editorial": "Diana",
			"año_publicacion": 1981,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Novela corta sobre un asesinato"
		},
		{
			"titulo": "El Código Da Vinci",
			"autor": ["Dan Brown"],
			"categoria": ["Thriller", "Misterio"],
			"precio": "44000.00",
			"stock": 45,
			"editorial": "Doubleday",
			"año_publicacion": 2003,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Thriller de conspiración religiosa"
		},
		{
			"titulo": "Python Programming E-Book",
			"autor": ["John Doe"],
			"categoria": ["Programación", "Tecnología"],
			"precio": "35000.00",
			"stock": 100,
			"editorial": "Tech Publishers",
			"año_publicacion": 2020,
			"idioma": "Español",
			"formato": "E-book",
			"descripcion": "Guía completa de Python"
		},
		{
			"titulo": "Mindfulness para Principiantes",
			"autor": ["Jon Kabat-Zinn"],
			"categoria": ["Autoayuda", "Bienestar"],
			"precio": "32000.00",
			"stock": 38,
			"editorial": "Kairós",
			"año_publicacion": 2016,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Introducción a la meditación mindfulness"
		},
		{
			"titulo": "La Sombra del Viento",
			"autor": ["Carlos Ruiz Zafón"],
			"categoria": ["Misterio", "Ficción"],
			"precio": "46000.00",
			"stock": 27,
			"editorial": "Planeta",
			"año_publicacion": 2001,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Misterio en la Barcelona de posguerra"
		},
		{
			"titulo": "El Alquimista",
			"autor": ["Paulo Coelho"],
			"categoria": ["Ficción", "Filosof\u00eda"],
			"precio": "36000.00",
			"stock": 42,
			"editorial": "HarperCollins",
			"año_publicacion": 1988,
			"idioma": "Español",
			"formato": "Tapa Blanda",
			"descripcion": "Fábula sobre seguir los sueños"
		},
		{
			"titulo": "El Hobbit",
			"autor": ["J.R.R. Tolkien"],
			"categoria": ["Fantasía", "Aventuras"],
			"precio": "52000.00",
			"stock": 33,
			"editorial": "George Allen & Unwin",
			"año_publicacion": 1937,
			"idioma": "Español",
			"formato": "Tapa Dura",
			"descripcion": "Precuela de El Señor de los Anillos"
		}
	]
	
	created_books = []
	for book_data in books_data:
		book = book_repo.create_book(**book_data)
		print(f"   ✅ Libro creado: {book.titulo} (Stock: {book.stock})")
		created_books.append(book)
	
	return created_books


def seed_inventory(db, books):
	"""Crear inventario para los libros"""
	print("\n📦 Creando inventario...")
	inventario_repo = InventarioRepository(db)
	
	for book in books:
		# Verificar si ya existe inventario
		existing = inventario_repo.get_inventario_by_libro(book.idlibro)
		if existing:
			print(f"   ⚠️  Inventario para '{book.titulo}' ya existe, omitiendo...")
			continue
		
		inventario = inventario_repo.create_inventario(
			idlibro=book.idlibro,
			stock_disponible=book.stock,
			umbral_minimo=max(5, book.stock // 10),  # 10% del stock o mínimo 5
			ubicacion_almacen=f"Estante {chr(65 + (book.idlibro % 26))}-{book.idlibro % 10 + 1}",
			notas="Inventario inicial"
		)
		print(f"   ✅ Inventario creado: {book.titulo} (Disponible: {inventario.stock_disponible}, Umbral: {inventario.umbral_minimo})")


def seed_carritos(db, users, books):
	"""Crear carritos de prueba"""
	print("\n🛒 Creando carritos...")
	carrito_repo = CarritoRepository(db)
	
	# Carrito activo para cliente
	cliente = next(u for u in users if u.rol == "CLIENTE")
	
	# Crear carrito vacío
	carrito1 = carrito_repo.create_carrito(
		idusuario=cliente.idusuario,
		sesion_id="sesion_001"
	)
	# Agregar items
	carrito_repo.add_item(carrito1, {
		"idlibro": books[0].idlibro,
		"cantidad": 2,
		"precio_unitario": str(books[0].precio),
		"subtotal_item": str(Decimal(books[0].precio) * 2)
	})
	carrito_repo.add_item(carrito1, {
		"idlibro": books[4].idlibro,
		"cantidad": 1,
		"precio_unitario": str(books[4].precio),
		"subtotal_item": str(books[4].precio)
	})
	carrito1 = carrito_repo.recalcular_totales(carrito1)
	print(f"   ✅ Carrito creado: Usuario {cliente.correo} - {len(carrito1.items)} items - Total: ${carrito1.total}")
	
	# Carrito completado (convertido en pedido)
	carrito2 = carrito_repo.create_carrito(
		idusuario=cliente.idusuario,
		sesion_id="sesion_002"
	)
	carrito_repo.add_item(carrito2, {
		"idlibro": books[2].idlibro,
		"cantidad": 1,
		"precio_unitario": str(books[2].precio),
		"subtotal_item": str(books[2].precio)
	})
	carrito2 = carrito_repo.recalcular_totales(carrito2)
	carrito2.estado = "CONVERTIDO"
	carrito_repo.update_carrito(carrito2)
	print(f"   ✅ Carrito creado: Usuario {cliente.correo} - CONVERTIDO")
	
	return [carrito1, carrito2]



def seed_pedidos(db, users, books):
	"""Crear pedidos de prueba"""
	print("\n📦 Creando pedidos...")
	pedido_repo = PedidoRepository(db)
	
	cliente = next(u for u in users if u.rol == "CLIENTE")
	
	# Pedido 1: Completado
	pedido1 = pedido_repo.create_pedido(
		idusuario=cliente.idusuario,
		items=[
			{
				"idlibro": books[2].idlibro,
				"titulo": books[2].titulo,
				"cantidad": 1,
				"precio_unitario": str(books[2].precio),
				"subtotal_item": str(books[2].precio)
			}
		],
		direccion_envio="Avenida Principal 456, Bogotá",
		metodo_pago="TARJETA_CREDITO",
		notas="Pedido de prueba - Entregado"
	)
	pedido1.estado = "COMPLETADO"
	pedido_repo.update_pedido(pedido1)
	print(f"   ✅ Pedido creado: #{pedido1.idpedido} - Estado: {pedido1.estado} - Total: ${pedido1.total}")
	
	# Pedido 2: En tránsito
	pedido2 = pedido_repo.create_pedido(
		idusuario=cliente.idusuario,
		items=[
			{
				"idlibro": books[5].idlibro,
				"titulo": books[5].titulo,
				"cantidad": 1,
				"precio_unitario": str(books[5].precio),
				"subtotal_item": str(books[5].precio)
			},
			{
				"idlibro": books[7].idlibro,
				"titulo": books[7].titulo,
				"cantidad": 1,
				"precio_unitario": str(books[7].precio),
				"subtotal_item": str(books[7].precio)
			}
		],
		direccion_envio="Avenida Principal 456, Bogotá",
		metodo_pago="PSE",
		notas="Pedido en camino"
	)
	pedido2.estado = "EN_TRANSITO"
	pedido_repo.update_pedido(pedido2)
	print(f"   ✅ Pedido creado: #{pedido2.idpedido} - Estado: {pedido2.estado} - Total: ${pedido2.total}")
	
	# Pedido 3: Pendiente
	pedido3 = pedido_repo.create_pedido(
		idusuario=cliente.idusuario,
		items=[
			{
				"idlibro": books[1].idlibro,
				"titulo": books[1].titulo,
				"cantidad": 2,
				"precio_unitario": str(books[1].precio),
				"subtotal_item": str(Decimal(books[1].precio) * 2)
			}
		],
		direccion_envio="Avenida Principal 456, Bogotá",
		metodo_pago="TARJETA_DEBITO",
		notas="Pedido reciente"
	)
	print(f"   ✅ Pedido creado: #{pedido3.idpedido} - Estado: {pedido3.estado} - Total: ${pedido3.total}")
	
	return [pedido1, pedido2, pedido3]


def seed_facturacion(db, users, pedidos):
	"""Crear facturas de prueba"""
	print("\n🧾 Creando facturas...")
	facturacion_repo = FacturacionRepository(db)
	
	cliente = next(u for u in users if u.rol == "CLIENTE")
	
	# Factura 1: Para pedido completado
	factura1 = facturacion_repo.create_factura(
		idpedido=pedidos[0].idpedido,
		idusuario=cliente.idusuario,
		metodo_pago=pedidos[0].metodo_pago,
		items=pedidos[0].items,
		datos_fiscales=f"NIT: 123456789 - {cliente.nombre} {cliente.apellido}",
		moneda="COP",
		notas="Factura pagada - Pedido completado"
	)
	factura1.estado = "PAGADA"
	facturacion_repo.update_factura(factura1)
	print(f"   ✅ Factura creada: #{factura1.idfactura} - Pedido #{factura1.idpedido} - Total: ${factura1.total}")
	
	# Factura 2: Para pedido en tránsito
	factura2 = facturacion_repo.create_factura(
		idpedido=pedidos[1].idpedido,
		idusuario=cliente.idusuario,
		metodo_pago=pedidos[1].metodo_pago,
		items=pedidos[1].items,
		datos_fiscales=f"NIT: 123456789 - {cliente.nombre} {cliente.apellido}",
		moneda="COP",
		notas="Factura pagada - En tránsito"
	)
	factura2.estado = "PAGADA"
	facturacion_repo.update_factura(factura2)
	print(f"   ✅ Factura creada: #{factura2.idfactura} - Pedido #{factura2.idpedido} - Total: ${factura2.total}")
	
	return [factura1, factura2]


def main():
	print("🚀 Iniciando carga de datos de prueba...\n")
	
	# Crear tablas si no existen
	Base.metadata.create_all(bind=engine)
	
	db = SessionLocal()
	try:
		users = seed_users(db)
		books = seed_books(db)
		seed_inventory(db, books)
		carritos = seed_carritos(db, users, books)
		pedidos = seed_pedidos(db, users, books)
		facturas = seed_facturacion(db, users, pedidos)
		
		print("\n✨ ¡Datos de prueba cargados exitosamente!")
		print(f"\n📊 Resumen:")
		print(f"   👥 Usuarios: {len(users)}")
		print(f"   📚 Libros: {len(books)}")
		print(f"   🛒 Carritos: {len(carritos)}")
		print(f"   📦 Pedidos: {len(pedidos)}")
		print(f"   🧾 Facturas: {len(facturas)}")
		print(f"\n🔐 Credenciales de prueba:")
		print(f"   Admin:     admin@libreria.com / admin123")
		print(f"   Cliente:   cliente@example.com / cliente123")
		print(f"   Vendedor:  vendedor@libreria.com / vendedor123")
		
	except Exception as e:
		print(f"\n❌ Error al cargar datos: {e}")
		db.rollback()
	finally:
		db.close()


if __name__ == "__main__":
	main()
