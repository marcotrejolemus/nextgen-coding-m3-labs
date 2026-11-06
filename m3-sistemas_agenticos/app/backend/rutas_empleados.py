"""Rutas de la API para la gestión de empleados."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from database import obtener_db
from esquemas import (
    DEPARTAMENTOS_VALIDOS,
    EmpleadoActualizar,
    EmpleadoBaja,
    EmpleadoCrear,
    EmpleadoRespuesta,
)
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


@router.get("/empleados", response_model=list[EmpleadoRespuesta])
def listar_empleados(
    busqueda: str | None = None,
    departamento: str | None = None,
    db: Session = Depends(obtener_db),
):
    consulta = db.query(Empleado)

    if busqueda:
        texto = f"%{busqueda.strip().lower()}%"
        consulta = consulta.filter(
            or_(
                func.lower(Empleado.nombre).like(texto),
                func.lower(Empleado.correo).like(texto),
            )
        )

    if departamento:
        consulta = consulta.filter(Empleado.departamento == departamento)

    return consulta.order_by(Empleado.id.asc()).all()


@router.get("/departamentos")
def listar_departamentos() -> list[str]:
    return DEPARTAMENTOS_VALIDOS


def _obtener_o_404(id: int, db: Session) -> Empleado:
    empleado = db.get(Empleado, id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.get("/empleados/{id}", response_model=EmpleadoRespuesta)
def obtener_empleado(id: int, db: Session = Depends(obtener_db)):
    return _obtener_o_404(id, db)


@router.put("/empleados/{id}", response_model=EmpleadoRespuesta)
def actualizar_empleado(id: int, datos: EmpleadoActualizar, db: Session = Depends(obtener_db)):
    empleado = _obtener_o_404(id, db)
    if empleado.estado == "baja":
        raise HTTPException(
            status_code=409, detail="No se puede editar a un empleado dado de baja"
        )

    empleado.puesto = datos.puesto
    empleado.departamento = datos.departamento
    db.commit()
    db.refresh(empleado)
    return empleado


@router.patch("/empleados/{id}/baja", response_model=EmpleadoRespuesta)
def dar_de_baja_empleado(id: int, datos: EmpleadoBaja, db: Session = Depends(obtener_db)):
    empleado = _obtener_o_404(id, db)
    if empleado.estado == "baja":
        raise HTTPException(status_code=409, detail="El empleado ya está dado de baja")
    if datos.fecha_baja < empleado.fecha_ingreso:
        raise HTTPException(
            status_code=422,
            detail="La fecha de baja no puede ser anterior a la fecha de ingreso",
        )

    empleado.estado = "baja"
    empleado.fecha_baja = datos.fecha_baja
    db.commit()
    db.refresh(empleado)
    return empleado
