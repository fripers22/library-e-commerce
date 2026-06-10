# Guía rápida de las capas del proyecto

Este proyecto está organizado por capas para separar responsabilidades y hacer el código más fácil de entender, mantener y probar. La idea es que cada carpeta tenga un trabajo claro y no mezcle lógica con otra que no le corresponde.

## `api`

Aquí viven los endpoints de FastAPI. Esta capa recibe las peticiones HTTP, valida lo básico de la entrada y devuelve respuestas al cliente.

En otras palabras, la carpeta `api` es la puerta de entrada de la aplicación. No debería tener reglas de negocio complejas ni consultas directas a la base de datos. Su trabajo es conectar la petición con el servicio correcto.

### Qué hace normalmente

- Define rutas como `GET`, `POST`, `PUT` y `DELETE`.
- Recibe datos desde el frontend o desde Postman.
- Usa `Depends` para obtener la base de datos o autenticación cuando hace falta.
- Llama a la capa `services` para ejecutar la lógica real.
- Devuelve respuestas HTTP con códigos y modelos de salida.

### Ejemplo mental

Si pides crear un usuario, la ruta de `api` recibe el formulario, llama al servicio y luego devuelve la respuesta final.

## `services`

Aquí va la lógica del negocio. Es la capa que decide qué se puede hacer y qué no, aplicando reglas, validaciones y flujos del negocio.

Si la `api` pregunta “qué hago con esta petición”, `services` responde “cómo se resuelve correctamente”.

### Qué hace normalmente

- Valida reglas del negocio, por ejemplo edades mínimas o campos obligatorios.
- Coordina varias operaciones de repositorio si hace falta.
- Decide si se lanza un error o si la operación continúa.
- Transforma datos antes de devolverlos.
- Mantiene la lógica fuera de los endpoints.

### Ejemplo mental

En este proyecto, un servicio de usuarios puede comprobar si el correo ya existe, si la contraseña es válida o si el usuario puede actualizarse.

## `repository`

Aquí está el acceso a datos. Esta capa sabe cómo hablar con la base de datos, pero no debería decidir reglas del negocio.

Su tarea es guardar, buscar, actualizar y borrar información. Es la parte más cercana a SQLAlchemy o al motor de base de datos.

### Qué hace normalmente

- Consulta registros por id, correo u otros filtros.
- Inserta nuevos objetos en la base de datos.
- Actualiza datos existentes.
- Elimina registros.
- Encapsula las consultas para que el resto del proyecto no dependa de SQL directo.

### Ejemplo mental

Si el servicio necesita buscar un usuario por correo, el repository es quien hace esa consulta.

## `domain`

Aquí están los modelos de datos que usa la aplicación para moverse entre capas. Normalmente se definen con Pydantic y sirven para validar y estructurar la información.

Esta carpeta representa los datos que entran y salen del sistema, por ejemplo lo que recibe un formulario y lo que devuelve la API.

### Qué hace normalmente

- Define modelos de entrada como `Create` o `Update`.
- Define modelos de salida como `Response`.
- Valida tipos de datos, campos requeridos y formatos.
- Evita que la API trabaje con diccionarios sueltos sin estructura.

### Ejemplo mental

Un modelo como `UserCreate` describe qué datos necesita la API para crear un usuario, y `UserResponse` define qué devolver cuando ya existe.

## Cómo se conectan entre sí

El flujo normal es este:

1. `api` recibe la petición HTTP.
2. `domain` valida y estructura los datos de entrada.
3. `services` aplica reglas de negocio.
4. `repository` consulta o modifica la base de datos.
5. `services` devuelve el resultado.
6. `api` responde al cliente.

## Forma fácil de recordarlo

- `api`: recibe y responde.
- `domain`: define la forma de los datos.
- `services`: decide la lógica del negocio.
- `repository`: habla con la base de datos.

## Para practicar otra vez

Si quieres repasar este tema, intenta responder estas preguntas sin mirar el código:

- ¿Qué pasaría si meto una regla de negocio dentro de `api`?
- ¿Por qué `repository` no debería validar si un usuario tiene 18 años?
- ¿Qué diferencia hay entre un modelo de `domain` y un objeto de la base de datos?
- ¿En qué capa debería estar una consulta SQL o una operación de búsqueda?

## Resumen corto

La arquitectura de este proyecto separa responsabilidades para que cada parte haga una sola cosa bien. Eso hace que el código sea más ordenado, más fácil de probar y más sencillo de modificar cuando el proyecto crece.