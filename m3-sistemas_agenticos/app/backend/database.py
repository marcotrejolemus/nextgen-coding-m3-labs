"""Configuración de la base de datos SQLite para la gestión de empleados."""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATOS_DIR = Path(__file__).resolve().parent / "datos"
DATOS_DIR.mkdir(exist_ok=True)

URL_BASE_DATOS = f"sqlite:///{DATOS_DIR / 'empleados.db'}"

engine = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def obtener_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
