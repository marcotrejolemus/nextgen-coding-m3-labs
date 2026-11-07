"""Pruebas de API para HU-10: solicitar vacaciones."""
import httpx


def test_cp_01_solicitud_valida_descuenta_dias_habiles(url_api, crear_empleado):
    """CP-01: Solicitud válida se registra y descuenta solo días hábiles."""
    empleado = crear_empleado(fecha_ingreso="2024-01-10")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-07-06", "fecha_fin": "2026-07-10"},
    )

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["dias_habiles"] == 5
    assert datos["dias_restantes"] == 7


def test_cp_03_usar_exactamente_el_saldo_restante(url_api, crear_empleado, registrar_vacacion):
    """CP-03: Se puede usar exactamente el saldo restante del año."""
    empleado = crear_empleado(fecha_ingreso="2023-05-02")
    registrar_vacacion(empleado["id"], "2026-01-05", "2026-01-09", 5)

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-07-13", "fecha_fin": "2026-07-21"},
    )

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["dias_habiles"] == 7
    assert datos["dias_restantes"] == 0


def test_cp_05_fines_de_semana_y_festivos_no_se_descuentan(url_api, crear_empleado):
    """CP-05: Los fines de semana y los festivos oficiales dentro del periodo no se descuentan."""
    empleado = crear_empleado(fecha_ingreso="2022-02-15")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-12-21", "fecha_fin": "2026-12-31"},
    )

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["dias_habiles"] == 8
    assert datos["dias_restantes"] == 4


def test_cp_07_error_antiguedad_insuficiente(url_api, crear_empleado):
    """CP-07: Error por antigüedad insuficiente."""
    empleado = crear_empleado(fecha_ingreso="2025-12-21")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-12-18", "fecha_fin": "2026-12-20"},
    )

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp_09_error_periodo_sin_dias_habiles(url_api, crear_empleado):
    """CP-09: Error cuando el periodo no incluye ningún día hábil."""
    empleado = crear_empleado(fecha_ingreso="2020-01-05")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-07-11", "fecha_fin": "2026-07-12"},
    )

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El periodo no incluye días hábiles"


def test_cp_11_error_rebasa_dias_disponibles(url_api, crear_empleado, registrar_vacacion):
    """CP-11: Error cuando la solicitud rebasa los días disponibles del año."""
    empleado = crear_empleado(fecha_ingreso="2019-03-01")
    registrar_vacacion(empleado["id"], "2026-01-05", "2026-01-08", 4)

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-08-03", "fecha_fin": "2026-08-13"},
    )

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "La solicitud excede los días disponibles: quedan 8 días hábiles"
    )


def test_cp_13_error_tope_anual_agotado(url_api, crear_empleado, registrar_vacacion):
    """CP-13: Error cuando el empleado ya agotó su tope anual."""
    empleado = crear_empleado(fecha_ingreso="2018-06-20")
    registrar_vacacion(empleado["id"], "2026-01-05", "2026-01-20", 12)

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-08-03", "fecha_fin": "2026-08-04"},
    )

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "La solicitud excede los días disponibles: quedan 0 días hábiles"
    )


def test_cp_15_error_fecha_fin_anterior_a_fecha_inicio(url_api, crear_empleado):
    """CP-15: Error cuando la fecha de fin es anterior a la fecha de inicio."""
    empleado = crear_empleado(fecha_ingreso="2021-04-11")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-07-10", "fecha_fin": "2026-07-05"},
    )

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "La fecha de fin no puede ser anterior a la fecha de inicio"
    )


def test_cp_17_error_periodo_cruza_de_anio(url_api, crear_empleado):
    """CP-17: Error cuando el periodo cruza de un año a otro."""
    empleado = crear_empleado(fecha_ingreso="2020-09-01")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-12-28", "fecha_fin": "2027-01-08"},
    )

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"]
        == "Las vacaciones deben estar dentro de un mismo año calendario"
    )


def test_cp_19_error_anio_sin_festivos_registrados(url_api, crear_empleado):
    """CP-19: Error cuando el año de la solicitud no está en la tabla de festivos."""
    empleado = crear_empleado(fecha_ingreso="2018-01-01")

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2025-07-01", "fecha_fin": "2025-07-05"},
    )

    assert respuesta.status_code == 400
    assert (
        respuesta.json()["detail"] == "Solo se pueden solicitar vacaciones en 2026 y 2027"
    )


def test_cp_21_error_empleado_no_existe(url_api):
    """CP-21: Error cuando el empleado no existe."""
    respuesta = httpx.post(
        f"{url_api}/api/empleados/9999/vacaciones",
        json={"fecha_inicio": "2026-07-06", "fecha_fin": "2026-07-10"},
    )

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Empleado no encontrado"


def test_cp_22_error_empleado_dado_de_baja(url_api, crear_empleado, marcar_empleado_baja):
    """CP-22: Error cuando el empleado está dado de baja."""
    empleado = crear_empleado(fecha_ingreso="2020-01-10")
    marcar_empleado_baja(empleado["numero_empleado"])

    respuesta = httpx.post(
        f"{url_api}/api/empleados/{empleado['id']}/vacaciones",
        json={"fecha_inicio": "2026-07-06", "fecha_fin": "2026-07-10"},
    )

    assert respuesta.status_code == 409
    assert (
        respuesta.json()["detail"]
        == "No se pueden solicitar vacaciones para un empleado dado de baja"
    )
