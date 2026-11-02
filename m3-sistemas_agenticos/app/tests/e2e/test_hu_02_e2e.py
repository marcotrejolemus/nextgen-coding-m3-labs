"""Pruebas E2E para HU-02: consultar el directorio de empleados."""
import uuid

from playwright.sync_api import expect


def test_cp_02_ver_directorio_completo(url_web, crear_empleado, marcar_empleado_baja, page):
    """CP-02: Camino feliz - ver el directorio completo."""
    sufijo = uuid.uuid4().hex[:8]
    ana = crear_empleado(
        nombre=f"Ana López {sufijo}",
        correo=f"ana.lopez.{sufijo}@empresa.com",
        puesto="Analista",
        departamento="Tecnología",
    )
    juan = crear_empleado(
        nombre=f"Juan Pérez {sufijo}",
        correo=f"juan.perez.{sufijo}@empresa.com",
        puesto="Gerente",
        departamento="Ventas",
    )
    marta = crear_empleado(
        nombre=f"Marta Ruiz {sufijo}",
        correo=f"marta.ruiz.{sufijo}@empresa.com",
        puesto="Contadora",
        departamento="Finanzas",
    )
    marcar_empleado_baja(marta["numero_empleado"])

    page.goto(url_web)

    for empleado, estado_esperado in ((ana, "Activo"), (juan, "Activo"), (marta, "Baja")):
        fila = page.get_by_test_id(f"fila-empleado-{empleado['id']}")
        expect(fila).to_be_visible()
        expect(page.get_by_test_id(f"numero-empleado-{empleado['id']}")).to_have_text(
            empleado["numero_empleado"]
        )
        expect(page.get_by_test_id(f"estado-empleado-{empleado['id']}")).to_have_text(
            estado_esperado
        )


def test_cp_04_buscar_por_nombre_sin_distinguir_mayusculas(url_web, crear_empleado, page):
    """CP-04: Buscar por nombre sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    nombre = f"Ana López {sufijo}"
    ana = crear_empleado(
        nombre=nombre,
        correo=f"ana.lopez.{sufijo}@empresa.com",
        puesto="Analista",
        departamento="Tecnología",
    )

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(nombre.upper())

    fila = page.get_by_test_id(f"fila-empleado-{ana['id']}")
    expect(fila).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{ana['id']}")).to_have_text(
        ana["numero_empleado"]
    )
    expect(page.locator('[data-testid^="fila-empleado-"]')).to_have_count(1)


def test_cp_06_buscar_por_correo_sin_distinguir_mayusculas(url_web, crear_empleado, page):
    """CP-06: Buscar por correo sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    correo = f"juan.perez.{sufijo}@empresa.com"
    juan = crear_empleado(
        nombre=f"Juan Pérez {sufijo}",
        correo=correo,
        puesto="Gerente",
        departamento="Ventas",
    )

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(correo.upper())

    fila = page.get_by_test_id(f"fila-empleado-{juan['id']}")
    expect(fila).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{juan['id']}")).to_have_text(
        juan["numero_empleado"]
    )
    expect(page.locator('[data-testid^="fila-empleado-"]')).to_have_count(1)


def test_cp_08_filtrar_por_departamento(url_web, crear_empleado, page):
    """CP-08: Filtrar por departamento."""
    sufijo = uuid.uuid4().hex[:8]
    marta = crear_empleado(
        nombre=f"Marta Ruiz {sufijo}",
        correo=f"marta.ruiz.{sufijo}@empresa.com",
        puesto="Contadora",
        departamento="Finanzas",
    )
    crear_empleado(
        nombre=f"Otro Empleado {sufijo}",
        correo=f"otro.{sufijo}@empresa.com",
        puesto="Analista",
        departamento="Tecnología",
    )

    page.goto(url_web)
    page.get_by_test_id("filtro-departamento").select_option("Finanzas")

    fila = page.get_by_test_id(f"fila-empleado-{marta['id']}")
    expect(fila).to_be_visible()
    expect(page.get_by_test_id(f"numero-empleado-{marta['id']}")).to_have_text(
        marta["numero_empleado"]
    )


def test_cp_10_buscar_texto_sin_coincidencias(url_web, crear_empleado, page):
    """CP-10: Buscar un texto que no coincide con ningún empleado."""
    sufijo = uuid.uuid4().hex[:8]
    crear_empleado(departamento="Operaciones")
    texto_sin_coincidencias = f"xyz-sin-coincidencias-{sufijo}"

    page.goto(url_web)
    page.get_by_test_id("buscar-empleados").fill(texto_sin_coincidencias)

    expect(page.get_by_test_id("sin-resultados")).to_have_text(
        "No se encontraron resultados"
    )
    expect(page.locator('[data-testid^="fila-empleado-"]')).to_have_count(0)


def test_cp_12_empleados_baja_aparecen_en_directorio(
    url_web, crear_empleado, marcar_empleado_baja, page
):
    """CP-12: Los empleados dados de baja siguen apareciendo en el directorio."""
    sufijo = uuid.uuid4().hex[:8]
    marta = crear_empleado(
        nombre=f"Marta Ruiz {sufijo}",
        correo=f"marta.ruiz.{sufijo}@empresa.com",
        puesto="Contadora",
        departamento="Finanzas",
    )
    marcar_empleado_baja(marta["numero_empleado"])

    page.goto(url_web)

    fila = page.get_by_test_id(f"fila-empleado-{marta['id']}")
    expect(fila).to_be_visible()
    expect(page.get_by_test_id(f"estado-empleado-{marta['id']}")).to_have_text("Baja")
    expect(page.get_by_test_id(f"numero-empleado-{marta['id']}")).to_have_text(
        marta["numero_empleado"]
    )
