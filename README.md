# 📝 Task Management API (FastAPI + PostgreSQL + Docker)

Este proyecto es una **API REST** profesional para la gestión de tareas, desarrollada con **FastAPI**. Implementa persistencia de datos en **PostgreSQL**, validación de esquemas con **Pydantic**, arquitectura de contenedores con **Docker Compose** y un sistema de registro de errores.

---

## 📂 Estructura del Proyecto

El código sigue una arquitectura modular para facilitar el mantenimiento y la escalabilidad:

* **app/main.py**: Punto de entrada de la aplicación. Gestiona las rutas (endpoints) y la configuración de FastAPI.
* **app/models.py**: Definición de modelos de base de datos (SQLAlchemy) y esquemas de validación (Pydantic). Contiene la lógica de creación de tablas.
* **app/service.py**: Capa de lógica de negocio y gestión del `TaskManager`.
* **docker-compose.yml**: Orquestación de servicios (API y Base de Datos).
* **Dockerfile**: Receta para construir la imagen de la aplicación Python.
* **requirements.txt**: Listado de librerías necesarias (FastAPI, SQLAlchemy, Psycopg2, etc.).
* **errores_api.log**: Archivo generado automáticamente para el registro de excepciones y fallos.

---

## 🚀 Guía de Ejecución con Docker

La forma más sencilla y recomendada de ejecutar este proyecto es utilizando Docker, lo que garantiza que la base de datos y la API se configuren correctamente de forma automática.

### 1. Construcción e Inicio
Desde la raíz del proyecto (donde se encuentra el archivo `docker-compose.yml`), ejecuta:

```bash
docker-compose up --build
```
Esto realizará las siguientes acciones:
* Levantará un contenedor con PostgreSQL 17.
* Construirá la imagen de la API instalando todas las dependencias.
* Esperará a que la base de datos esté lista e iniciará el servidor Uvicorn.

### 2. Acceso a la API

Una vez que los contenedores estén en marcha, puedes interactuar con la API en:

Documentación Interactiva (Swagger): 
```bash
http://localhost:8000/docs
```

### 3. Detener el Entorno
Para apagar los servicios y limpiar los recursos:
```bash
docker-compose down
```

## 🛠️ Consideraciones de Diseño (POO y Lógica)
El proyecto se ha desarrollado siguiendo principios de **programación Orientada a Objetos** (POO) y una arquitectura de capas que garantiza una separación clara de responsabilidades:
### 1. Organización en Capas
* **Models**: Define la estructura de los datos y las reglas de integridad (ej: títulos obligatorios, validación de fechas).
* **Service (TaskManager)**: Encapsula la lógica de negocio. Es el único componente que interactúa directamente con la base de datos a través de SQLAlchemy.
* **Main (Router)**: Actúa como controlador, recibiendo peticiones HTTP y delegando la ejecución al servicio correspondiente.

### 2. Persistencia y Validación
* **PostgreSQL**: Se utiliza una base de datos relacional robusta en lugar de archivos locales, gestionada mediante variables de entorno en Docker.
* **Pydantic (DTO)**: Se utilizan modelos diferenciados para la creación (`TaskCreate`) y la respuesta (`TaskResponse`). Esto protege la integridad de los datos y asegura que el usuario solo reciba la información necesaria.

### 3. Resiliencia y Logs
* **Control de Errores**: La aplicación captura excepciones operacionales y de lógica de negocio, devolviendo códigos de estado HTTP semánticos (`400`, `404`, `500`).
* **Logging**: Todos los errores críticos se registran en el archivo `errores_api.log` dentro del contenedor, facilitando la depuración en entornos de producción.
* **Wait-for-DB**: El sistema incluye una estrategia de espera (*sleep/retry*) en el arranque para asegurar que la API no intente conectar con la base de datos antes de que esta haya terminado su proceso de inicialización.

## 🔀 Cambios principales realizados:
1.  **Tecnología**: Cambié SQLite por **PostgreSQL**.
2.  **Despliegue**: Sustituí los pasos de `venv` y `uvicorn` local por los comandos de **Docker Compose**, que es como lo estás ejecutando ahora.
3.  **Rutas**: Actualicé la descripción de la estructura de archivos para reflejar el uso de `Dockerfile` y `docker-compose.yml`.
4.  **Logs**: Mantuve la mención al archivo de logs pero contextualizada en el entorno de contenedores.
