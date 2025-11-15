# Library API - Sistema de E-Commerce para Librería

API REST desarrollada con FastAPI siguiendo arquitectura en capas (Clean Architecture) para gestionar un sistema completo de e-commerce de librería incluyendo usuarios, libros, carritos de compra, pedidos, facturación e inventario.

## 🏗️ Arquitectura

- **API Layer** (`app/api/`): Endpoints REST y routers
- **Service Layer** (`app/services/`): Lógica de negocio y validaciones
- **Repository Layer** (`app/repository/`): Acceso a datos con SQLAlchemy
- **Domain Layer** (`app/domain/`): Modelos Pydantic (DTOs) y validaciones
- **Database** (`app/database.py`): Modelos SQLAlchemy ORM

## 📋 Requisitos

- Python 3.11+
- SQLite (incluido en Python)

## 🚀 Instalación

1. Crear y activar entorno virtual:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Instalar dependencias:
```powershell
pip install -r requirements.txt
```

3. (Opcional) Cargar datos de prueba:
```powershell
python scripts/seed_data.py
```

4. Ejecutar la aplicación:
```powershell
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`

## 📖 Documentación

- **Swagger UI**: `http://127.0.0.1:8000/docs` (interactiva)
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para autenticación:

### Login
```bash
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=cliente@example.com&password=cliente123
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "idusuario": 2,
  "nombre": "Carlos",
  "correo": "cliente@example.com",
  "rol": "CLIENTE"
}
```

Usar el token en requests:
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Roles
- **ADMIN**: Acceso completo al sistema
- **VENDEDOR**: Gestión de inventario y pedidos
- **CLIENTE**: Compras y consulta de productos

## 🔌 Endpoints Principales

### 🔑 Autenticación (`/auth`)
- `POST /auth/login` - Autenticarse y obtener token JWT

### 👥 Usuarios (`/usuarios`)
- `POST /usuarios/` - Crear usuario (registro)
- `POST /usuarios/verificar/{token}` - Verificar email
- `POST /usuarios/enviar-verificacion/{id}` - Reenviar token de verificación
- `GET /usuarios/` - Listar usuarios
- `GET /usuarios/{id}` - Obtener usuario
- `PUT /usuarios/{id}` - Actualizar usuario
- `DELETE /usuarios/{id}` - Eliminar usuario

### 📚 Libros (`/libros`)
- `POST /libros/` - Crear libro
- `GET /libros/` - Listar libros
- `GET /libros/{id}` - Obtener libro
- `PUT /libros/{id}` - Actualizar libro
- `DELETE /libros/{id}` - Eliminar libro

### 🛒 Carritos (`/carritos`)
- `POST /carritos/` - Crear carrito
- `GET /carritos/usuario/{id}` - Obtener carrito del usuario
- `POST /carritos/{id}/items` - Agregar item al carrito
- `DELETE /carritos/{id}/items/{idlibro}` - Quitar item del carrito
- `PUT /carritos/{id}/estado` - Actualizar estado del carrito
- `DELETE /carritos/{id}` - Eliminar carrito

### 📦 Pedidos (`/pedidos`)
- `POST /pedidos/` - Crear pedido desde carrito
- `GET /pedidos/` - Listar pedidos
- `GET /pedidos/{id}` - Obtener pedido
- `GET /pedidos/usuario/{id}` - Pedidos de un usuario
- `PUT /pedidos/{id}` - Actualizar estado del pedido
- `DELETE /pedidos/{id}` - Cancelar pedido

### 🧾 Facturación (`/facturacion`)
- `POST /facturacion/` - Crear factura para un pedido
- `GET /facturacion/` - Listar facturas
- `GET /facturacion/{id}` - Obtener factura
- `GET /facturacion/pedido/{id}` - Obtener factura de un pedido
- `GET /facturacion/usuario/{id}` - Facturas de un usuario
- `PUT /facturacion/{id}` - Actualizar factura
- `DELETE /facturacion/{id}` - Eliminar factura

### 📊 Inventario (`/inventario`)
- `POST /inventario/` - Crear registro de inventario
- `GET /inventario/` - Listar inventario
- `GET /inventario/{id}` - Obtener inventario por ID
- `GET /inventario/libro/{id}` - Inventario de un libro
- `PUT /inventario/{id}` - Actualizar inventario
- `DELETE /inventario/{id}` - Eliminar registro

## ✅ Validaciones de Negocio

### Usuarios
- Email único y formato válido
- Edad mínima: 18 años
- Contraseña encriptada con bcrypt
- Email debe ser verificado para activar cuenta
- Roles: CLIENTE, VENDEDOR, ADMIN

### Libros
- Título y autor requeridos
- Precio positivo
- Stock no negativo
- Año válido (1000-2100)
- Categorías y autores como listas
- Formatos: Tapa Dura, Tapa Blanda, E-book

### Carritos
- Un carrito activo por usuario
- Verificación de stock antes de agregar items
- Cálculo automático de subtotales, IVA (19%) y totales
- Estados: ACTIVO, ABANDONADO, CONVERTIDO

### Pedidos
- Creación desde carrito existente
- Validación de stock al crear pedido
- Reducción automática de inventario
- Estados: PENDIENTE, EN_TRANSITO, COMPLETADO, CANCELADO
- Métodos de pago: TARJETA_CREDITO, TARJETA_DEBITO, PSE, EFECTIVO

### Facturación
- Vinculada a un pedido único
- Incluye datos fiscales del cliente
- Cálculo automático de impuestos
- Estados: EMITIDA, PAGADA, ANULADA
- Soporte de múltiples monedas (default: COP)

### Inventario
- Vinculado a un libro
- Seguimiento de stock disponible y reservado
- Alertas de stock bajo (umbral configurable)
- Actualizaciones automáticas al crear/cancelar pedidos

## 🗃️ Base de Datos

SQLite (`library.db`) con 6 tablas:

- **users**: Usuarios del sistema (clientes, vendedores, admins)
- **books**: Catálogo de libros
- **carritos**: Carritos de compra
- **pedidos**: Órdenes de compra
- **facturacion**: Facturas generadas
- **inventario**: Control de stock

## 🧪 Datos de Prueba

Ejecutar `python scripts/seed_data.py` para cargar:

**Usuarios:**
- Admin: `admin@libreria.com` / `admin123`
- Cliente: `cliente@example.com` / `cliente123`
- Vendedor: `vendedor@libreria.com` / `vendedor123`

**Datos cargados:**
- 3 usuarios (todos verificados y activos)
- 15 libros de diversos géneros
- 15 registros de inventario
- 2 carritos de ejemplo
- 3 pedidos (COMPLETADO, EN_TRANSITO, PENDIENTE)
- 2 facturas (para pedidos completados/en tránsito)

## 🔄 Flujo de Compra Completo

1. **Registro/Login**
   - Cliente se registra: `POST /usuarios/`
   - Verifica email: `POST /usuarios/verificar/{token}`
   - Login: `POST /auth/login` → Obtiene JWT

2. **Agregar Productos al Carrito**
   - Crear carrito: `POST /carritos/` (automático si no existe)
   - Agregar items: `POST /carritos/{id}/items`
   - Ver carrito: `GET /carritos/usuario/{id}`

3. **Realizar Pedido**
   - Crear pedido: `POST /pedidos/` (desde carrito)
   - Carrito cambia a estado "CONVERTIDO"
   - Inventario se reduce automáticamente

4. **Facturación**
   - Generar factura: `POST /facturacion/` (para el pedido)
   - Consultar factura: `GET /facturacion/pedido/{id}`

5. **Seguimiento**
   - Ver pedidos: `GET /pedidos/usuario/{id}`
   - Actualizar estado: `PUT /pedidos/{id}` (vendedor/admin)

## 📦 Estructura del Proyecto

```
libreria-api/
├── app/
│   ├── api/                    # Endpoints REST
│   │   ├── auth_api.py        # Autenticación JWT
│   │   ├── user_api.py        # Gestión de usuarios
│   │   ├── book_api.py        # Gestión de libros
│   │   ├── carrito_api.py     # Carritos de compra
│   │   ├── pedido_api.py      # Pedidos
│   │   ├── facturacion_api.py # Facturación
│   │   └── inventario_api.py  # Inventario
│   ├── config/
│   │   └── routers.py         # Registro de routers
│   ├── domain/                # Modelos Pydantic
│   ├── repository/            # Acceso a datos
│   ├── services/              # Lógica de negocio
│   ├── auth.py                # JWT y autenticación
│   ├── database.py            # Modelos SQLAlchemy
│   └── main.py                # App FastAPI
├── scripts/
│   └── seed_data.py           # Script de datos de prueba
├── tests/                     # 27 tests automatizados
│   ├── test_usuarios.py
│   ├── test_libros.py
│   ├── test_carritos.py
│   └── test_flujo_completo.py
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

## 🛠️ Tecnologías

- **FastAPI** 0.121.2 - Framework web moderno y rápido
- **SQLAlchemy** 2.0.22 - ORM para Python
- **Pydantic** 2.12.4[email] - Validación de datos
- **python-jose[cryptography]** 3.3.0 - JWT
- **passlib[bcrypt]** 1.7.4 - Hash de contraseñas
- **python-multipart** 0.0.20 - OAuth2
- **Uvicorn** 0.38.0 - Servidor ASGI
- **pytest** 9.0.1 - Testing
- **SQLite** - Base de datos

## 🧪 Testing

Ejecutar tests:
```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Cobertura:
- 27 tests automatizados
- Pruebas unitarias y de integración
- Validación de flujos completos de compra

## 🚀 Funcionalidades Implementadas

✅ Sistema de usuarios con roles (CLIENTE, VENDEDOR, ADMIN)  
✅ Autenticación JWT con tokens de 30 minutos  
✅ Verificación de email con tokens UUID  
✅ Hash de contraseñas con bcrypt  
✅ Catálogo de libros con múltiples atributos  
✅ Carritos de compra con cálculo automático de IVA  
✅ Sistema de pedidos con estados  
✅ Facturación electrónica  
✅ Control de inventario con alertas  
✅ Validaciones de negocio completas  
✅ Tests automatizados (27 tests passing)  
✅ Script de datos de prueba  
✅ Documentación interactiva (Swagger UI)  

## ⚠️ Notas de Producción

- **SECRET_KEY**: Cambiar `SECRET_KEY` en `app/auth.py` a un valor seguro
- **Base de Datos**: Migrar a PostgreSQL/MySQL para producción
- **CORS**: Configurar orígenes permitidos en producción
- **HTTPS**: Usar certificados SSL/TLS
- **Variables de Entorno**: Mover configuraciones sensibles a `.env`

## 📝 Licencia

Este proyecto es un sistema educativo/demo de e-commerce para librerías.
