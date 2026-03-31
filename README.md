# 📝 Task Management API (FastAPI + SQLAlchemy)

Este proyecto es una **API REST** profesional para la gestión de tareas, desarrollada con **FastAPI**. Implementa persistencia de datos en **SQLite**, validación de esquemas con **Pydantic** y un sistema de pruebas automatizado..

---

## 📂 Estructura del Proyecto

El código sigue una arquitectura modular para facilitar el mantenimiento y la escalabilidad:

* **app/main.py**: Punto de entrada de la aplicación. Gestiona las rutas (endpoints) y la inyección de dependencias.
* **app/models.py**: Definición de modelos de base de datos (SQLAlchemy) y esquemas de validación (Pydantic).
* **app/service.py**: 
* **tasks.db**: Base de datos de producción (SQLite).
* **test_api.py**: Suite de pruebas completa que valida el CRUD, duplicados y reglas de negocio.
* **seed_db.py**: Script para poblar la base de datos con ejemplos que demuestran algunos puntos clave de la práctica.
* **requirements.txt**: Dependencias: Listado de librerías necesarias para el proyecto.
---

## 🚀 Guía de Ejecución

### 1. Configuración del Entorno Virtual
Es recomendable usar un entorno virtual para aislar las dependencias del proyecto:

En Windows:
```bash
# Crear el entorno
python -m venv venv
# Activarlo
.\venv\Scripts\activate
```
En macOS/Linux:
```bash
# Crear el entorno
python3 -m venv venv
# Activarlo
source venv/bin/activate
```

### 2. Instalación de Dependencias
Una vez activado el entorno, instala todos los paquetes necesarios utilizando el archivo de requerimientos:
```bash
pip install -r requirements.txt
```

### 3. Ejecución del Servidor
Para lanzar la API:
```bash
uvicorn app.main:app --reload
```
La base de datos tasks.db se generará automáticamente al iniciar. Puedes acceder a la documentación interactiva en http://127.0.0.1:8000/docs

### 4. Poblado de Datos (Opcional)
Si deseas probar la API con datos de ejemplo rápidamente, hemos incluido un script para rellenar la base de datos con tareas de prueba (algunas de ellas ya caducadas para probar los filtros):
```bash
python app/seed.py
```

### 5. Ejecución de Tests
Para validar que todo funciona correctamente sin afectar a los datos reales:
En Windows (PowerShell)
```bash
$env:TESTING="True"; python app/test_api.py
```
En macOS/Linux:
```bash
TESTING=True python3 app/test_api.py
```
Tras las pruebas las tareas generadas en el paso 4 deberían ser las unicas en la base de datos.

## 🛠️ Consideraciones de Diseño (POO y Lógica)
El proyecto se ha desarrollado siguiendo principios de **Programación Orientada a Objetos (POO)** y una arquitectura de capas que garantiza una separación clara de responsabilidades:

1. **Organización en Capas (Separación de tareas)**: En lugar de tener todo en un solo archivo, hemos repartido el trabajo para que el código sea más limpio:
    - models.py: Define cómo son los datos y qué reglas deben cumplir (ej: el título es obligatorio, la fecha no puede ser pasada).
    - service.py: Contiene la lógica de negocio. Aquí es donde se crean, borran o marcan como completadas las tareas en la base de datos.
    - main.py: Recibe las peticiones del usuario, le pregunta al servidor (service.py) qué hacer y devuelve la respuesta final.

2. **Uso de Objetos y Validación (POO)**: 
    - TaskManager: Hemos encapsulado todas las operaciones de la base de datos dentro de esta clase. Así, el resto del programa no necesita saber "cómo" se guarda una tarea, solo tiene que pedírselo al Manager.
    - Modelos de Entrada y Salida (DTO): Diferenciamos entre TaskCreate (lo que el usuario envía) y TaskResponse (lo que la API devuelve). Esto permite filtrar información sensible (como IDs internos o metadatos) y validar reglas de negocio (como que el deadline no sea una fecha pasada) antes de tocar la base de datos.

3. **Control de Errores y Logs**: 
    - Registro de fallos: Todos los errores importantes (como intentar crear una tarea que ya existe) se guardan automáticamente en un archivo llamado errores_api.log.

    - Mensajes claros: Si el usuario envía datos mal formados, la API responde con un mensaje sencillo explicando exactamente qué campo está mal.




# INFO ADICIONAL ORIGINAL DEL ENUNCIADO

## Instalación

### 1. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Puedes usar cualquiera de estos comandos:

```bash
# Opción 1: Comando moderno de FastAPI
fastapi app/main.py

# Opción 2: Uvicorn tradicional
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Endpoints

### TODO: Documentar todos los endpoints

- `GET /` - Información de la API
- `POST /tasks/` - Crear una nueva tarea
- `GET /tasks/{task_id}` - Obtener una tarea por ID
- `PUT /tasks/{task_id}/completar` - Marcar una tarea como completada
- `GET /tasks/caducadas` - Obtener lista de tareas caducadas

## Ejecutar tests

```bash
python test_api.py
```

## Documentación interactiva

Una vez ejecutando la aplicación, puedes acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
