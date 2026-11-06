# language: es
Característica: Editar y dar de baja a un empleado
  Como persona del área de Recursos Humanos
  quiero cambiar el puesto y el departamento de un empleado, y poder darlo de baja,
  para mantener el directorio al día sin perder el historial.

  Escenario: Editar puesto y departamento de un empleado activo
    Dado que existe el empleado "EMP-0007" con puesto "Analista" y departamento "Ventas" y estado "activo"
    Cuando edito el empleado "EMP-0007" con puesto "Analista Senior" y departamento "Tecnología"
    Entonces el sistema responde 200
    Y el empleado "EMP-0007" tiene puesto "Analista Senior" y departamento "Tecnología"

  Escenario: Dar de baja a un empleado activo
    Dado que existe el empleado "EMP-0008" con estado "activo" y fecha_ingreso "2022-01-10"
    Cuando doy de baja al empleado "EMP-0008" con fecha_baja "2024-05-01"
    Entonces el sistema responde 200
    Y el empleado "EMP-0008" tiene estado "baja" y fecha_baja "2024-05-01"
    Y el empleado "EMP-0008" sigue apareciendo en el directorio

  Escenario: No editar el número de empleado ni el correo
    Dado que existe el empleado "EMP-0009" con numero_empleado "EMP-0009" y correo "ana.perez@empresa.com"
    Cuando intento editar el empleado "EMP-0009" enviando numero_empleado "EMP-9999" y correo "nuevo@empresa.com"
    Entonces el sistema responde 200
    Y el empleado "EMP-0009" conserva numero_empleado "EMP-0009" y correo "ana.perez@empresa.com"

  Escenario: Error al editar un empleado dado de baja
    Dado que existe el empleado "EMP-0010" con estado "baja"
    Cuando intento editar el empleado "EMP-0010" con puesto "Gerente"
    Entonces el sistema responde 409 con el mensaje "No se puede editar a un empleado dado de baja"

  Escenario: Error al editar con un departamento no permitido
    Dado que existe el empleado "EMP-0011" con estado "activo" y departamento "Finanzas"
    Cuando edito el empleado "EMP-0011" con departamento "Marketing"
    Entonces el sistema responde 422
    Y la pantalla indica que el campo "departamento" debe corregirse

  Escenario: Error al dar de baja con una fecha de baja anterior a la fecha de ingreso
    Dado que existe el empleado "EMP-0012" con estado "activo" y fecha_ingreso "2023-03-01"
    Cuando doy de baja al empleado "EMP-0012" con fecha_baja "2023-01-15"
    Entonces el sistema responde 422 con el mensaje "La fecha de baja no puede ser anterior a la fecha de ingreso"

# Preguntas abiertas
# - No se especifica si enviar numero_empleado o correo al editar debe generar un error (p. ej. 422) o simplemente ignorarse y responder 200 sin cambios en esos campos. Se asumió la segunda opción (escenario 3); confirmar con el dueño del producto.
# - No se especifica el mensaje exacto que debe mostrar el sistema cuando fecha_baja es anterior a fecha_ingreso. Se infirió el texto "La fecha de baja no puede ser anterior a la fecha de ingreso" siguiendo el patrón de otros mensajes de la regla de negocio; confirmar redacción exacta.
