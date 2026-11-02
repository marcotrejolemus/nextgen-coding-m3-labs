"""Pruebas de API para HU-02: consultar el directorio de empleados."""
import uuid

import httpx


def test_cp_01_ver_directorio_completo(url_api, crear_empleado, marcar_empleado_baja):
    """CP-01: Camino feliz - ver el directorio completo."""
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

    respuesta = httpx.get(f"{url_api}/api/empleados")

    assert respuesta.status_code == 200
    empleados = {empleado["correo"]: empleado for empleado in respuesta.json()}

    assert empleados[ana["correo"]]["numero_empleado"] == ana["numero_empleado"]
    assert empleados[ana["correo"]]["puesto"] == "Analista"
    assert empleados[ana["correo"]]["departamento"] == "Tecnología"
    assert empleados[ana["correo"]]["estado"] == "activo"

    assert empleados[juan["correo"]]["numero_empleado"] == juan["numero_empleado"]
    assert empleados[juan["correo"]]["puesto"] == "Gerente"
    assert empleados[juan["correo"]]["departamento"] == "Ventas"
    assert empleados[juan["correo"]]["estado"] == "activo"

    assert empleados[marta["correo"]]["numero_empleado"] == marta["numero_empleado"]
    assert empleados[marta["correo"]]["puesto"] == "Contadora"
    assert empleados[marta["correo"]]["departamento"] == "Finanzas"
    assert empleados[marta["correo"]]["estado"] == "baja"


def test_cp_03_buscar_por_nombre_sin_distinguir_mayusculas(url_api, crear_empleado):
    """CP-03: Buscar por nombre sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    nombre = f"Ana López {sufijo}"
    creado = crear_empleado(
        nombre=nombre,
        correo=f"ana.lopez.{sufijo}@empresa.com",
        puesto="Analista",
        departamento="Tecnología",
    )

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"busqueda": nombre.upper()})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    assert len(resultados) == 1
    assert resultados[0]["correo"] == creado["correo"]
    assert resultados[0]["numero_empleado"] == creado["numero_empleado"]
    assert resultados[0]["puesto"] == "Analista"
    assert resultados[0]["departamento"] == "Tecnología"
    assert resultados[0]["estado"] == "activo"


def test_cp_05_buscar_por_correo_sin_distinguir_mayusculas(url_api, crear_empleado):
    """CP-05: Buscar por correo sin distinguir mayúsculas de minúsculas."""
    sufijo = uuid.uuid4().hex[:8]
    correo = f"juan.perez.{sufijo}@empresa.com"
    creado = crear_empleado(
        nombre=f"Juan Pérez {sufijo}",
        correo=correo,
        puesto="Gerente",
        departamento="Ventas",
    )

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"busqueda": correo.upper()})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    assert len(resultados) == 1
    assert resultados[0]["correo"] == correo
    assert resultados[0]["numero_empleado"] == creado["numero_empleado"]
    assert resultados[0]["puesto"] == "Gerente"
    assert resultados[0]["departamento"] == "Ventas"
    assert resultados[0]["estado"] == "activo"


def test_cp_07_filtrar_por_departamento(url_api, crear_empleado):
    """CP-07: Filtrar por departamento."""
    sufijo = uuid.uuid4().hex[:8]
    marta = crear_empleado(
        nombre=f"Marta Ruiz {sufijo}",
        correo=f"marta.ruiz.{sufijo}@empresa.com",
        puesto="Contadora",
        departamento="Finanzas",
    )
    otro = crear_empleado(
        nombre=f"Otro Empleado {sufijo}",
        correo=f"otro.{sufijo}@empresa.com",
        puesto="Analista",
        departamento="Tecnología",
    )

    respuesta = httpx.get(f"{url_api}/api/empleados", params={"departamento": "Finanzas"})

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    correos = [empleado["correo"] for empleado in resultados]
    assert marta["correo"] in correos
    assert otro["correo"] not in correos

    empleado = next(e for e in resultados if e["correo"] == marta["correo"])
    assert empleado["numero_empleado"] == marta["numero_empleado"]
    assert empleado["puesto"] == "Contadora"
    assert empleado["departamento"] == "Finanzas"


def test_cp_09_buscar_texto_sin_coincidencias(url_api, crear_empleado):
    """CP-09: Buscar un texto que no coincide con ningún empleado."""
    sufijo = uuid.uuid4().hex[:8]
    crear_empleado(departamento="Operaciones")
    texto_sin_coincidencias = f"xyz-sin-coincidencias-{sufijo}"

    respuesta = httpx.get(
        f"{url_api}/api/empleados", params={"busqueda": texto_sin_coincidencias}
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_cp_11_empleados_baja_aparecen_en_directorio(
    url_api, crear_empleado, marcar_empleado_baja
):
    """CP-11: Los empleados dados de baja siguen apareciendo en el directorio."""
    sufijo = uuid.uuid4().hex[:8]
    marta = crear_empleado(
        nombre=f"Marta Ruiz {sufijo}",
        correo=f"marta.ruiz.{sufijo}@empresa.com",
        puesto="Contadora",
        departamento="Finanzas",
    )
    marcar_empleado_baja(marta["numero_empleado"])

    respuesta = httpx.get(f"{url_api}/api/empleados")

    assert respuesta.status_code == 200
    resultados = respuesta.json()
    empleado = next(e for e in resultados if e["correo"] == marta["correo"])
    assert empleado["estado"] == "baja"
    assert empleado["numero_empleado"] == marta["numero_empleado"]
    assert empleado["nombre"] == marta["nombre"]
    assert empleado["puesto"] == "Contadora"
    assert empleado["departamento"] == "Finanzas"
