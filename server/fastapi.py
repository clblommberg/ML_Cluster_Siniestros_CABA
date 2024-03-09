# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from server.conexion import SessionLocal, engine
from models import Homicidios as HomicidiosModel
from pydantic import BaseModel, BaseConfig
from typing import List, Optional
from datetime import datetime


import pandas as pd
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method
import os 

from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# Configura CORS (si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto según tu configuración
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definición de los modelos Pydantic para validación de datos
class HomicidiosBase(BaseModel):
    id: str
    n_victimas: int
    lugar_del_hecho: Optional[str]
    tipo_de_calle: Optional[str]
    direccion_normalizada: Optional[str]
    comuna: int
    pos_x: Optional[float]
    pos_y: Optional[float]
    acusado: Optional[str]
    anio: Optional[int]
    mes: Optional[int]
    dia: Optional[int]
    fecha_hora: Optional[str]
    fecha_formato: Optional[str]
    hora_formato: Optional[str]
    hora_i: Optional[int]
    coordenada_x: Optional[float]
    coordenada_y: Optional[float]

class PropiedadCreate(HomicidiosBase):
    pass

class PropiedadUpdate(HomicidiosBase):
    pass

class Propiedad(HomicidiosBase):
    id: int
    published_on: datetime

    class Config:
        orm_mode = True

# Obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Operaciones CRUD para Persona
db_dependency = Depends(get_db)



# Obtener todas las propiedades
@app.get("/propiedades/", response_model=List[Propiedad])
async def read_all_propiedades(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    propiedades = db.query(HomicidiosModel).offset(skip).limit(limit).all()
    return propiedades

# Crear una nueva propiedad
@app.post("/propiedades/", response_model=Propiedad)
async def create_propiedad(propiedad: PropiedadCreate, db: Session = Depends(get_db)):
    db_propiedad = HomicidiosModel(**propiedad.dict())
    db.add(db_propiedad)
    db.commit()
    db.refresh(db_propiedad)
    return db_propiedad

# Obtener detalles de una propiedad por ID
@app.get("/propiedades/{propiedad_id}", response_model=Propiedad)
async def read_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    db_propiedad = db.query(HomicidiosModel).filter(HomicidiosModel.id == propiedad_id).first()
    if db_propiedad is None:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return db_propiedad

# Actualizar una propiedad por ID
@app.put("/propiedades/{propiedad_id}", response_model=Propiedad)
async def update_propiedad(propiedad_id: int, propiedad: PropiedadUpdate, db: Session = Depends(get_db)):
    db_propiedad = db.query(HomicidiosModel).filter(HomicidiosModel.id == propiedad_id).first()
    if db_propiedad is None:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")

    # Actualizar campos de la propiedad
    for var, value in vars(propiedad).items():
        setattr(db_propiedad, var, value) if value else None

    db.commit()
    db.refresh(db_propiedad)
    return db_propiedad

# Eliminar una propiedad por ID
@app.delete("/propiedades/{propiedad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    db_propiedad = db.query(HomicidiosModel).filter(HomicidiosModel.id == propiedad_id).first()
    if db_propiedad is None:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")

    db.delete(db_propiedad)
    db.commit()
    return {}
