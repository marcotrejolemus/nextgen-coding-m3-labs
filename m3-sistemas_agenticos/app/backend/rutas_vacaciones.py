"""Rutas de la API para solicitar y consultar vacaciones (HU-10)."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import obtener_db
from esquemas import VacacionCrear, VacacionRespuesta, VacacionSaldo
from modelos import Vacacion
from rutas_empleados import _obtener_o_404
from vacaciones import (
    DIAS_DISPONIBLES_POR_ANIO,
    anio_tiene_festivos,
    cumple_antiguedad,
    dias_habiles_en_periodo,
)

router = APIRouter()


def _dias_usados_en_anio(db: Session, empleado_id: int, anio: int) -> int:
    solicitudes = (
        db.query(Vacacion)
        .filter(
            Vacacion.empleado_id == empleado_id,
            Vacacion.fecha_inicio >= date(anio, 1, 1),
            Vacacion.fecha_inicio <= date(anio, 12, 31),
        )
        .all()
    )
    return sum(solicitud.dias_habiles for solicitud in solicitudes)


@router.post(
    "/empleados/{id}/vacaciones", response_model=VacacionRespuesta, status_code=201
)
def solicitar_vacaciones(
    id: int, datos: VacacionCrear, db: Session = Depends(obtener_db)
):
    empleado = _obtener_o_404(id, db)
    if empleado.estado == "baja":
        raise HTTPException(
            status_code=409,
            detail="No se pueden solicitar vacaciones para un empleado dado de baja",
        )
    if datos.fecha_fin < datos.fecha_inicio:
        raise HTTPException(
            status_code=400,
            detail="La fecha de fin no puede ser anterior a la fecha de inicio",
        )
    if datos.fecha_inicio.year != datos.fecha_fin.year:
        raise HTTPException(
            status_code=400,
            detail="Las vacaciones deben estar dentro de un mismo año calendario",
        )
    anio = datos.fecha_inicio.year
    if not anio_tiene_festivos(anio):
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden solicitar vacaciones en 2026 y 2027",
        )
    if not cumple_antiguedad(empleado.fecha_ingreso, datos.fecha_inicio):
        raise HTTPException(
            status_code=400,
            detail="Se requiere al menos un año de antigüedad a la fecha de inicio",
        )

    dias_habiles = dias_habiles_en_periodo(datos.fecha_inicio, datos.fecha_fin)
    if dias_habiles == 0:
        raise HTTPException(
            status_code=400, detail="El periodo no incluye días hábiles"
        )

    dias_usados = _dias_usados_en_anio(db, id, anio)
    dias_disponibles = DIAS_DISPONIBLES_POR_ANIO - dias_usados
    if dias_habiles > dias_disponibles:
        raise HTTPException(
            status_code=400,
            detail=(
                "La solicitud excede los días disponibles: "
                f"quedan {dias_disponibles} días hábiles"
            ),
        )

    vacacion = Vacacion(
        empleado_id=id,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        dias_habiles=dias_habiles,
    )
    db.add(vacacion)
    db.commit()
    db.refresh(vacacion)

    return VacacionRespuesta(
        id=vacacion.id,
        empleado_id=vacacion.empleado_id,
        fecha_inicio=vacacion.fecha_inicio,
        fecha_fin=vacacion.fecha_fin,
        dias_habiles=vacacion.dias_habiles,
        dias_restantes=dias_disponibles - dias_habiles,
    )


@router.get("/empleados/{id}/vacaciones", response_model=VacacionSaldo)
def consultar_saldo_vacaciones(
    id: int, anio: int | None = None, db: Session = Depends(obtener_db)
):
    _obtener_o_404(id, db)
    anio_consulta = anio or date.today().year

    solicitudes = (
        db.query(Vacacion)
        .filter(
            Vacacion.empleado_id == id,
            Vacacion.fecha_inicio >= date(anio_consulta, 1, 1),
            Vacacion.fecha_inicio <= date(anio_consulta, 12, 31),
        )
        .order_by(Vacacion.fecha_inicio.asc())
        .all()
    )
    dias_usados = sum(solicitud.dias_habiles for solicitud in solicitudes)

    return VacacionSaldo(
        empleado_id=id,
        anio=anio_consulta,
        dias_usados=dias_usados,
        dias_disponibles=DIAS_DISPONIBLES_POR_ANIO - dias_usados,
        solicitudes=solicitudes,
    )
