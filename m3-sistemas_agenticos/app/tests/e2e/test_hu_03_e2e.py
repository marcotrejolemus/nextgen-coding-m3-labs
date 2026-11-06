"""Pruebas E2E para HU-03: editar datos de un empleado y darlo de baja."""
import httpx
from playwright.sync_api import expect


def test_cp_02_editar_puesto_y_departamento(url_web, crear_empleado, page):
    """CP-02: Editar puesto y departamento de un empleado activo."""
    empleado = crear_empleado(puesto="Analista", departamento="Ventas")

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{empleado['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("Analista Senior")
    page.get_by_test_id("empleado-departamento").select_option("Tecnología")
    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    fila = page.get_by_test_id(f"fila-empleado-{empleado['id']}")
    expect(fila).to_contain_text("Analista Senior")
    expect(fila).to_contain_text("Tecnología")


def test_cp_04_dar_de_baja_empleado_activo(url_web, crear_empleado, page):
    """CP-04: Dar de baja a un empleado activo."""
    empleado = crear_empleado(fecha_ingreso="2022-01-10")

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{empleado['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2024-05-01")
    page.get_by_test_id("confirmar-baja").click()

    expect(page.get_by_test_id("mensaje-exito")).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{empleado['id']}")).to_have_text("Baja")
    expect(page.get_by_test_id(f"fila-empleado-{empleado['id']}")).to_be_visible()


def test_cp_07_error_al_editar_empleado_dado_de_baja(url_api, url_web, crear_empleado, page):
    """CP-07: Error al editar un empleado dado de baja."""
    empleado = crear_empleado(departamento="Tecnología")
    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{empleado['id']}/baja",
        json={"fecha_baja": "2024-01-15"},
    )
    assert respuesta.status_code == 200

    page.goto(url_web)
    expect(page.get_by_test_id(f"estado-empleado-{empleado['id']}")).to_have_text("Baja")
    page.get_by_test_id(f"editar-empleado-{empleado['id']}").click()
    page.get_by_test_id("empleado-puesto").fill("Gerente")
    page.get_by_test_id("empleado-guardar").click()

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "No se puede editar a un empleado dado de baja"
    )


def test_cp_09_error_al_editar_con_departamento_no_permitido(url_web, crear_empleado, page):
    """CP-09: Error al editar con un departamento no permitido.

    El <select> de empleado-departamento solo ofrece los departamentos que
    devuelve GET /api/departamentos, así que no existe una opción "Marketing"
    que se pueda elegir desde la interfaz (ver nota del automatizador). Se
    verifica que esa opción inválida no está disponible para seleccionar.
    """
    empleado = crear_empleado(departamento="Finanzas")

    page.goto(url_web)
    page.get_by_test_id(f"editar-empleado-{empleado['id']}").click()
    select = page.get_by_test_id("empleado-departamento")
    expect(select.locator("option", has_text="Marketing")).to_have_count(0)


def test_cp_11_error_fecha_baja_anterior_a_fecha_ingreso(url_web, crear_empleado, page):
    """CP-11: Error al dar de baja con una fecha de baja anterior a la fecha de ingreso."""
    empleado = crear_empleado(fecha_ingreso="2023-03-01")

    page.goto(url_web)
    page.get_by_test_id(f"baja-empleado-{empleado['id']}").click()
    page.get_by_test_id("empleado-fecha-baja").fill("2023-01-15")
    page.get_by_test_id("confirmar-baja").click()

    expect(page.get_by_test_id("mensaje-error")).to_have_text(
        "La fecha de baja no puede ser anterior a la fecha de ingreso"
    )
