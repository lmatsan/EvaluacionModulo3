import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional

#CONFIGURACIÓN DE LA BASE DE DATOS
# Si no existe la variable, os.environ[] lanzará un KeyError, 
# lo cual es perfecto para detectar errores de configuración en Docker.
SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
        )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MODELO DE BASE DE DATOS (SQLAlchemy)
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=True, index=True, nullable=False)
    contenido = Column(String)
    deadline = Column(Date)
    completada = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.now)

# CREAR LAS TABLAS EN EL ARCHIVO .DB
Base.metadata.create_all(bind=engine)

# MODELOS DE VALIDACIÓN Y RESPUESTA (Pydantic)
# TaskCreate: Define los datos que exigimos al usuario para 
#             crear una nueva tarea (Validación de entrada).
# TaskUpdate: Define qué campos permitimos modificar en una 
#             tarea existente (Edición parcial).
# TaskResponse: Define la estructura de los datos que devolvemos 
#             al cliente (Esquema de salida).
class TaskCreate(BaseModel):
    titulo: str = Field(min_length=1, description="Título de la tarea")
    contenido: str = Field(min_length=1, description="Contenido de la tarea")
    deadline: date = Field(description="Fecha de vencimiento")

    @field_validator('deadline')
    @classmethod
    def deadline_must_be_future(cls, v: date):
        if v < date.today():
            raise ValueError('El deadline no puede ser una fecha pasada')
        return v

class TaskUpdate(BaseModel):
    completada: bool = Field(description="Estado de completado")

class TaskUpdateField(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    # Solo definimos tipos; la validación estricta ya se hizo en 
    # TaskCreate al recibir el dato.
    id: int
    titulo: str 
    contenido: str 
    deadline: date 
    completada: bool 
    fecha_creacion: datetime 
    model_config = {
        "from_attributes": True, "str_strip_whitespace": True
    }
