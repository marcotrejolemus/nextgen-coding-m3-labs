"""Reglas de negocio de vacaciones (HU-10), separadas de las rutas HTTP."""
from datetime import date, timedelta

DIAS_DISPONIBLES_POR_ANIO = 12

FESTIVOS: dict[int, set[date]] = {
    2026: {
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 16),
        date(2026, 5, 1),
        date(2026, 9, 16),
        date(2026, 11, 16),
        date(2026, 12, 25),
    },
    2027: {
        date(2027, 1, 1),
        date(2027, 2, 1),
        date(2027, 3, 15),
        date(2027, 5, 1),
        date(2027, 9, 16),
        date(2027, 11, 15),
        date(2027, 12, 25),
    },
}


def anio_tiene_festivos(anio: int) -> bool:
    return anio in FESTIVOS


def dias_habiles_en_periodo(inicio: date, fin: date) -> int:
    """Cuenta los días del periodo (incluyendo inicio y fin) que no son
    sábado, domingo ni festivo oficial."""
    total = 0
    dia = inicio
    while dia <= fin:
        festivos_anio = FESTIVOS.get(dia.year, set())
        if dia.weekday() < 5 and dia not in festivos_anio:
            total += 1
        dia += timedelta(days=1)
    return total


def fecha_primer_aniversario(fecha_ingreso: date) -> date:
    """Fecha en la que se cumple exactamente un año de antigüedad. Si el
    ingreso fue un 29 de febrero, el aniversario en un año no bisiesto cae
    el 1 de marzo."""
    try:
        return fecha_ingreso.replace(year=fecha_ingreso.year + 1)
    except ValueError:
        return date(fecha_ingreso.year + 1, 3, 1)


def cumple_antiguedad(fecha_ingreso: date, fecha_inicio: date) -> bool:
    return fecha_inicio >= fecha_primer_aniversario(fecha_ingreso)
