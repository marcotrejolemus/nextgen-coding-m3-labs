# language: es
Característica: Registrar empleado
  Como persona del área de Recursos Humanos
  Quiero registrar a un empleado con su nombre, correo corporativo, puesto, departamento y fecha de ingreso
  Para darlo de alta en la empresa

  Escenario: Registro exitoso de un empleado con datos válidos
    Dado que no existe ningún empleado con correo "ana.perez@empresa.com"
    Cuando registro un empleado con los siguientes datos:
      | nombre       | Ana Pérez                 |
      | correo       | ana.perez@empresa.com     |
      | puesto       | Analista de Datos         |
      | departamento | Tecnología                |
      | fecha_ingreso| 2024-01-15                |
    Entonces el sistema responde con código 201
    Y el empleado queda registrado con estado "activo"
    Y el sistema asigna un número de empleado con formato "EMP-0001"
    Y la pantalla muestra un mensaje de confirmación con el número de empleado asignado

  Escenario: No se permite registrar un empleado con un correo ya registrado
    Dado que ya existe un empleado registrado con correo "ana.perez@empresa.com"
    Cuando intento registrar un empleado con correo "ANA.PEREZ@EMPRESA.COM"
    Entonces el sistema responde con código 409
    Y la pantalla muestra el mensaje "El correo ya está registrado"

  Escenario: No se permite registrar un empleado con correo no corporativo
    Dado que no existe ningún empleado con correo "ana.perez@gmail.com"
    Cuando intento registrar un empleado con correo "ana.perez@gmail.com"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "Usa el correo corporativo @empresa.com"

  Escenario: No se permite registrar un empleado con fecha de ingreso futura
    Dado que la fecha actual del sistema es "2024-06-01"
    Cuando intento registrar un empleado con fecha de ingreso "2999-01-01"
    Entonces el sistema responde con código 422
    Y la pantalla muestra el mensaje "La fecha de ingreso no puede ser futura"

  Esquema del escenario: No se permite registrar un empleado con otros datos inválidos
    Cuando intento registrar un empleado con <campo> "<valor>"
    Entonces el sistema responde con código 422
    Y la pantalla muestra qué campo corregir: "<campo>"

    Ejemplos:
      | campo        | valor      |
      | nombre       | A          |
      | puesto       | X          |
      | departamento | Marketing  |

# Preguntas abiertas
# - No se especifica el mensaje exacto que debe mostrarse para cada campo inválido bajo la regla 3
#   (nombre, puesto, departamento). Se asumió un mensaje genérico "qué campo corregir" según la regla de negocio,
#   pero se recomienda definir el texto exacto para nombre, puesto y departamento.
# - No se especifica el comportamiento cuando falta un campo obligatorio (nombre, correo, puesto, fecha_ingreso
#   vacíos). Se asume que cae bajo la regla 3 (422, indicar campo a corregir), pero no hay mensaje específico.
