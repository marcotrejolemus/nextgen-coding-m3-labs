"""Fixtures compartidas para las pruebas de la aplicación de gestión de empleados."""
import os
import sqlite3
import uuid
from pathlib import Path

import httpx
import pytest

RUTA_BASE_DATOS = Path(__file__).resolve().parent.parent / "backend" / "datos" / "empleados.db"


@pytest.fixture
def url_api() -> str:
    return os.environ.get("URL_API", "http://localhost:8000")


@pytest.fixture
def url_web() -> str:
    return os.environ.get("URL_WEB", "http://localhost:8080")


@pytest.fixture
def crear_empleado(url_api):
    """Crea un empleado vía la API con datos únicos y permite sobreescribir campos."""

    def _crear(**overrides) -> dict:
        sufijo = uuid.uuid4().hex[:8]
        payload = {
            "nombre": f"Empleado Prueba {sufijo}",
            "correo": f"empleado.{sufijo}@empresa.com",
            "puesto": "Analista",
            "departamento": "Tecnología",
            "fecha_ingreso": "2024-01-10",
        }
        payload.update(overrides)
        respuesta = httpx.post(f"{url_api}/api/empleados", json=payload)
        assert respuesta.status_code == 201, respuesta.text
        return respuesta.json()

    return _crear


@pytest.fixture
def registrar_vacacion():
    """Inserta una solicitud de vacaciones directamente en la base de datos.

    Sirve para preparar precondiciones de HU-10 (saldo ya usado en el año)
    sin depender del endpoint de creación, que es justamente lo que prueban
    los casos de esta historia.
    """

    def _registrar(empleado_id: int, fecha_inicio: str, fecha_fin: str, dias_habiles: int) -> None:
        conexion = sqlite3.connect(RUTA_BASE_DATOS)
        try:
            conexion.execute(
                "INSERT INTO vacaciones (empleado_id, fecha_inicio, fecha_fin, dias_habiles) "
                "VALUES (?, ?, ?, ?)",
                (empleado_id, fecha_inicio, fecha_fin, dias_habiles),
            )
            conexion.commit()
        finally:
            conexion.close()

    return _registrar


@pytest.fixture
def marcar_empleado_baja():
    """Marca un empleado como baja escribiendo directamente en la base de datos.

    HU-02 no expone ningún endpoint para dar de baja (eso es HU-03), así que
    las precondiciones con empleados en estado "baja" se preparan aquí.
    """

    def _marcar(numero_empleado: str, fecha_baja: str = "2024-01-15") -> None:
        conexion = sqlite3.connect(RUTA_BASE_DATOS)
        try:
            conexion.execute(
                "UPDATE empleados SET estado = 'baja', fecha_baja = ? WHERE numero_empleado = ?",
                (fecha_baja, numero_empleado),
            )
            conexion.commit()
        finally:
            conexion.close()

    return _marcar
