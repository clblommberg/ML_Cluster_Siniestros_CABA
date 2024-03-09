from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from conexion import Base, engine

from sqlalchemy.orm import declarative_base
class Homicidios(Base):
    __tablename__ = "homicidios_h"

    id = Column(String, primary_key=True)
    n_victimas = Column(Integer)
    lugar_del_hecho = Column(String)
    tipo_de_calle = Column(String)
    direccion_normalizada = Column(String)
    comuna = Column(Integer)
    pos_x = Column(Float)
    pos_y = Column(Float)
    acusado = Column(String)
    anio = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    fecha_hora = Column(DateTime)
    fecha_formato = Column(String)
    hora_formato = Column(String)
    hora_i = Column(Integer)
    coordenada_x = Column(Float)
    coordenada_y = Column(Float)

class Victimas(Base):
    __tablename__ = "victimas_l"
    id = Column(Integer, primary_key=True, index=True)
    id_hecho = Column(String)
    rol = Column(String)
    victima = Column(String)
    sexo = Column(String)
    edad = Column(String)
    fecha_fallecimiento = Column(DateTime)

class Comunas(Base):
    __tablename__ = "comunas_l"
    id = Column(Integer, primary_key=True, index=True)
    objeto = Column(String)
    comunas = Column(Integer)
    barrios = Column(String)
    perimetro = Column(Float)
    area = Column(Float)

# Aquí se crea la tabla en la base de datos si no existe
Base.metadata.create_all(bind=engine)
