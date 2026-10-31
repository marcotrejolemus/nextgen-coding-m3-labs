"""Esquemas Pydantic v2 de la gestión de empleados."""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

DEPARTAMENTOS_VALIDOS = [
    "Tecnología",
    "Ventas",
    "Finanzas",
    "Recursos Humanos",
    "Operaciones",
]


class EmpleadoCrear(BaseModel):
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        if not (2 <= len(valor.strip()) <= 80):
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres")
        return valor.strip()

    @field_validator("puesto")
    @classmethod
    def validar_puesto(cls, valor: str) -> str:
        if not (2 <= len(valor.strip()) <= 60):
            raise ValueError("El puesto debe tener entre 2 y 60 caracteres")
        return valor.strip()

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor: str) -> str:
        valor = valor.strip().lower()
        if not valor.endswith("@empresa.com"):
            raise ValueError("Usa el correo corporativo @empresa.com")
        return valor

    @field_validator("departamento")
    @classmethod
    def validar_departamento(cls, valor: str) -> str:
        if valor not in DEPARTAMENTOS_VALIDOS:
            raise ValueError(
                "El departamento debe ser uno de: " + ", ".join(DEPARTAMENTOS_VALIDOS)
            )
        return valor

    @field_validator("fecha_ingreso")
    @classmethod
    def validar_fecha_ingreso(cls, valor: date) -> date:
        if valor > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        return valor


class EmpleadoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_empleado: str
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date
    estado: str
    fecha_baja: date | None
    creado_en: datetime
