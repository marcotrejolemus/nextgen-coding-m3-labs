"""Pruebas E2E para HU-10: solicitar vacaciones."""
from playwright.sync_api import expect


def test_cp_02_solicitud_valida_descuenta_dias_habiles(url_web, crear_empleado, page):
    """CP-02: Solicitud válida se registra y descuenta solo días hábiles."""
    empleado = crear_empleado(fecha_ingreso="2024-01-10")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-07-06")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-07-10")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 5 días hábiles. Te quedan 7 días hábiles en 2026."
    )


def test_cp_04_usar_exactamente_el_saldo_restante(
    url_web, crear_empleado, registrar_vacacion, page
):
    """CP-04: Se puede usar exactamente el saldo restante del año."""
    empleado = crear_empleado(fecha_ingreso="2023-05-02")
    registrar_vacacion(empleado["id"], "2026-01-05", "2026-01-09", 5)

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-07-13")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-07-21")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 7 días hábiles. Te quedan 0 días hábiles en 2026."
    )


def test_cp_06_fines_de_semana_y_festivos_no_se_descuentan(url_web, crear_empleado, page):
    """CP-06: Los fines de semana y los festivos oficiales dentro del periodo no se descuentan."""
    empleado = crear_empleado(fecha_ingreso="2022-02-15")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-12-21")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-12-31")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solicitud registrada: 8 días hábiles. Te quedan 4 días hábiles en 2026."
    )


def test_cp_08_error_antiguedad_insuficiente(url_web, crear_empleado, page):
    """CP-08: Error por antigüedad insuficiente."""
    empleado = crear_empleado(fecha_ingreso="2025-12-21")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-12-18")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-12-20")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Se requiere al menos un año de antigüedad a la fecha de inicio"
    )


def test_cp_10_error_periodo_sin_dias_habiles(url_web, crear_empleado, page):
    """CP-10: Error cuando el periodo no incluye ningún día hábil."""
    empleado = crear_empleado(fecha_ingreso="2020-01-05")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-07-11")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-07-12")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "El periodo no incluye días hábiles"
    )


def test_cp_12_error_rebasa_dias_disponibles(
    url_web, crear_empleado, registrar_vacacion, page
):
    """CP-12: Error cuando la solicitud rebasa los días disponibles del año."""
    empleado = crear_empleado(fecha_ingreso="2019-03-01")
    registrar_vacacion(empleado["id"], "2026-01-05", "2026-01-08", 4)

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-08-03")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-08-13")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "La solicitud excede los días disponibles: quedan 8 días hábiles"
    )


def test_cp_14_error_tope_anual_agotado(url_web, crear_empleado, registrar_vacacion, page):
    """CP-14: Error cuando el empleado ya agotó su tope anual."""
    empleado = crear_empleado(fecha_ingreso="2018-06-20")
    registrar_vacacion(empleado["id"], "2026-01-05", "2026-01-20", 12)

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-08-03")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-08-04")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "La solicitud excede los días disponibles: quedan 0 días hábiles"
    )


def test_cp_16_error_fecha_fin_anterior_a_fecha_inicio(url_web, crear_empleado, page):
    """CP-16: Error cuando la fecha de fin es anterior a la fecha de inicio."""
    empleado = crear_empleado(fecha_ingreso="2021-04-11")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-07-10")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2026-07-05")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "La fecha de fin no puede ser anterior a la fecha de inicio"
    )


def test_cp_18_error_periodo_cruza_de_anio(url_web, crear_empleado, page):
    """CP-18: Error cuando el periodo cruza de un año a otro."""
    empleado = crear_empleado(fecha_ingreso="2020-09-01")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2026-12-28")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2027-01-08")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Las vacaciones deben estar dentro de un mismo año calendario"
    )


def test_cp_20_error_anio_sin_festivos_registrados(url_web, crear_empleado, page):
    """CP-20: Error cuando el año de la solicitud no está en la tabla de festivos."""
    empleado = crear_empleado(fecha_ingreso="2018-01-01")

    page.goto(url_web)
    page.get_by_test_id(f"vacaciones-abrir-{empleado['id']}").click()
    page.get_by_test_id("vacaciones-fecha-inicio").fill("2025-07-01")
    page.get_by_test_id("vacaciones-fecha-fin").fill("2025-07-05")
    page.get_by_test_id("vacaciones-enviar").click()

    expect(page.get_by_test_id("vacaciones-mensaje")).to_have_text(
        "Solo se pueden solicitar vacaciones en 2026 y 2027"
    )
