"""Pruebas de API para HU-03: editar datos de un empleado y darlo de baja."""
import httpx


def test_cp_01_editar_puesto_y_departamento(url_api, crear_empleado):
    """CP-01: Editar puesto y departamento de un empleado activo."""
    empleado = crear_empleado(puesto="Analista", departamento="Ventas")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['id']}",
        json={"puesto": "Analista Senior", "departamento": "Tecnología"},
    )
    assert respuesta.status_code == 200

    respuesta = httpx.get(f"{url_api}/api/empleados/{empleado['id']}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["puesto"] == "Analista Senior"
    assert datos["departamento"] == "Tecnología"


def test_cp_03_dar_de_baja_empleado_activo(url_api, crear_empleado):
    """CP-03: Dar de baja a un empleado activo."""
    empleado = crear_empleado(fecha_ingreso="2022-01-10")

    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{empleado['id']}/baja",
        json={"fecha_baja": "2024-05-01"},
    )
    assert respuesta.status_code == 200

    respuesta = httpx.get(f"{url_api}/api/empleados/{empleado['id']}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["estado"] == "baja"
    assert datos["fecha_baja"] == "2024-05-01"

    respuesta = httpx.get(f"{url_api}/api/empleados")
    assert respuesta.status_code == 200
    numeros = [empleado_listado["numero_empleado"] for empleado_listado in respuesta.json()]
    assert empleado["numero_empleado"] in numeros


def test_cp_05_no_editar_numero_empleado_ni_correo(url_api, crear_empleado):
    """CP-05: No editar el número de empleado ni el correo."""
    empleado = crear_empleado(puesto="Analista", departamento="Ventas")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['id']}",
        json={
            "puesto": empleado["puesto"],
            "departamento": empleado["departamento"],
            "numero_empleado": "EMP-9999",
            "correo": "nuevo@empresa.com",
        },
    )
    assert respuesta.status_code == 200

    respuesta = httpx.get(f"{url_api}/api/empleados/{empleado['id']}")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["numero_empleado"] == empleado["numero_empleado"]
    assert datos["correo"] == empleado["correo"]


def test_cp_06_error_al_editar_empleado_dado_de_baja(url_api, crear_empleado):
    """CP-06: Error al editar un empleado dado de baja."""
    empleado = crear_empleado(departamento="Tecnología")
    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{empleado['id']}/baja",
        json={"fecha_baja": "2024-01-15"},
    )
    assert respuesta.status_code == 200

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['id']}",
        json={"puesto": "Gerente", "departamento": "Tecnología"},
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["detail"] == "No se puede editar a un empleado dado de baja"


def test_cp_08_error_al_editar_con_departamento_no_permitido(url_api, crear_empleado):
    """CP-08: Error al editar con un departamento no permitido."""
    empleado = crear_empleado(departamento="Finanzas")

    respuesta = httpx.put(
        f"{url_api}/api/empleados/{empleado['id']}",
        json={"departamento": "Marketing"},
    )
    assert respuesta.status_code == 422


def test_cp_10_error_fecha_baja_anterior_a_fecha_ingreso(url_api, crear_empleado):
    """CP-10: Error al dar de baja con una fecha de baja anterior a la fecha de ingreso."""
    empleado = crear_empleado(fecha_ingreso="2023-03-01")

    respuesta = httpx.patch(
        f"{url_api}/api/empleados/{empleado['id']}/baja",
        json={"fecha_baja": "2023-01-15"},
    )
    assert respuesta.status_code == 422
    assert (
        respuesta.json()["detail"]
        == "La fecha de baja no puede ser anterior a la fecha de ingreso"
    )
