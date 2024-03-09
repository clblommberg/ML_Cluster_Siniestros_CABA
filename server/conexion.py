# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Lee el archivo CSV

# Utiliza la URL correcta para PostgreSQL
URL_DATABASE = "postgresql+psycopg2://postgres:mailito@localhost:5432/siniestros"
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

