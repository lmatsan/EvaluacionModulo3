from sqlalchemy.orm import Session
from datetime import date
from .models import TaskDB, TaskCreate, TaskUpdateField 

class TaskManager:
    def __init__(self, db: Session):
        self.db = db
        self.__palabras_prohibidas = ["feo", "malo", "tonto"]

    def _process_text(self, texto: str) -> str:
        if not texto:
            return texto
        limpio = texto.strip().lower()
        # Censura de palabras
        for palabra in self.__palabras_prohibidas:
            limpio = limpio.replace(palabra, "*" * len(palabra))
            
        return limpio.capitalize()

    def exist_by_title(self, titulo: str) -> bool:
        return self.db.query(TaskDB).filter(TaskDB.titulo == titulo).first() is not None

    def create_new_task(self, task_data: TaskCreate) -> TaskDB:
        contenido_censurado = self._process_text(task_data.contenido)
        nueva_tarea = TaskDB(
            titulo=task_data.titulo,
            contenido=contenido_censurado,
            deadline=task_data.deadline
        )
        self.db.add(nueva_tarea)
        self.db.commit()
        self.db.refresh(nueva_tarea)
        return nueva_tarea

    def get_task_by_id(self, task_id: int) -> TaskDB | None:
        return self.db.query(TaskDB).filter(TaskDB.id == task_id).first()

    def mark_as_completed(self, task_id: int) -> TaskDB | None:
        tarea = self.get_task_by_id(task_id)
        if tarea:
            tarea.completada = True
            self.db.commit()
            self.db.refresh(tarea)
        return tarea

    def get_expired_tasks(self) -> list[TaskDB]:
        # Lógica para filtrar tareas cuya fecha es anterior a hoy 
        hoy = date.today()
        tareas = self.db.query(TaskDB).filter(
            TaskDB.deadline < hoy,
            TaskDB.completada == False
        ).all()
        # REST Standard: Una búsqueda sin resultados debe devolver 
        # lista vacía [] (200 OK), reservando el error 404 solo 
        # para cuando un ID específico no existe.
        return tareas

    def delete_task(self, task_id: int) -> bool:
        tarea = self.get_task_by_id(task_id)
        if tarea:
            self.db.delete(tarea)
            self.db.commit()
            return True
        return False
    
    def get_all_tasks(self) -> list[TaskDB]:
        return self.db.query(TaskDB).all()

    def update_task(self, db: Session, task_id: int, task_data: TaskUpdateField) -> TaskDB | None:
        db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not db_task:
            return None
        
        # Se Actualizan solo los campos que vengan en la petición
        update_data = task_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task