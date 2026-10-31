"""Rutas de la API para la gestión de empleados."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import obtener_db
from esquemas import DEPARTAMENTOS_VALIDOS, EmpleadoCrear, EmpleadoRespuesta
from modelos import Empleado

router = APIRouter()


def _generar_numero_empleado(db: Session) -> str:
    total = db.query(func.count(Empleado.id)).scalar() or 0
    return f"EMP-{total + 1:04d}"


@router.post("/empleados", response_model=EmpleadoRespuesta, status_code=201)
def registrar_empleado(datos: EmpleadoCrear, db: Session = Depends(obtener_db)):
    existente = db.query(Empleado).filter(Empleado.correo == datos.correo).first()
    if existente:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    empleado = Empleado(
        numero_empleado=_generar_numero_empleado(db),
        nombre=datos.nombre,
        correo=datos.correo,
        puesto=datos.puesto,
        departamento=datos.departamento,
        fecha_ingreso=datos.fecha_ingreso,
        estado="activo",
    )
    db.add(empleado)
    db.commit()
    db.refresh(empleado)
    return empleado


@router.get("/departamentos")
def listar_departamentos() -> list[str]:
    return DEPARTAMENTOS_VALIDOS
