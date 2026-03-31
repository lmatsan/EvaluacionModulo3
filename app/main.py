from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
#from pydantic import BaseModel, Field, field_validator
from typing import List
from fastapi.responses import JSONResponse
import logging

# IMPORTACIONES DE NUESTROS NUEVOS ARCHIVOS
from .models import Base, engine, TaskCreate, TaskResponse, SessionLocal
from .service import TaskManager

# INICIALIZACIÓN
app = FastAPI(title="APITask", description="API para la gestión de tareas", version="1.0.0")
Base.metadata.create_all(bind=engine) #Crea las tablas al arrancar

# CONFIGURACIÓN DE LOGS
logging.basicConfig(
    filename='errores_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

# MANEJADOR DE ERRORES
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    friendly_message = error.get("msg")
    affected_field = error.get("loc")[-1]

    # GUARDAR EN EL ARCHIVO LOG
    logging.warning(f"Validation error in '{affected_field}': {friendly_message}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid data",
            "message": f"{error['loc'][-1]}: {error['msg']}"
        }
    )


# Implementacion endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS DE LA API
@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(task: TaskCreate, db=Depends(get_db)):
    if TaskManager(db).exist_by_title(task.titulo):
        # Registramos el intento en el log
        logging.warning(f"Intento de tarea duplicada: {task.titulo}")
        # Lanzamos una excepción de FastAPI
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una tarea con este título"
        )

    nueva_tarea = TaskManager(db).create_new_task(task)

    return nueva_tarea 

@app.get("/tasks/caducadas", response_model=List[TaskResponse])
def obtener_tareas_caducadas(db=Depends(get_db)):
    tareas = TaskManager(db).get_expired_tasks()
    
    return tareas

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def obtener_tarea(task_id: int, db=Depends(get_db)):
    tarea = TaskManager(db).get_task_by_id(task_id)

    if not tarea:
        logging.warning(f"Consulta fallida: Tarea con ID {task_id} no encontrada.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La tarea con ID {task_id} no existe"
        )
    
    return tarea


@app.put("/tasks/{task_id}/completar", response_model=TaskResponse)
def marcar_completada(task_id: int, db=Depends(get_db)):
    tarea_actualizada = TaskManager(db).mark_as_completed(task_id)

    if not tarea_actualizada:
        logging.warning(f"Intento de completar tarea inexistente: ID {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontró la tarea con el ID proporcionado"
        )

    return tarea_actualizada

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(task_id: int, db=Depends(get_db)):
    if not TaskManager(db).delete_task(task_id):
        raise HTTPException(status_code=404, detail="No se pudo eliminar: Tarea no encontrada")
    return None # El código 204 no devuelve cuerpo

@app.get("/")
def root():
    return {"message": "Task Management API"}