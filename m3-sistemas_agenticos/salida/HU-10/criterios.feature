# language: es

Característica: Solicitar vacaciones
  Como empleado de la empresa
  Quiero solicitar días de vacaciones indicando una fecha de inicio y una de fin
  Para que mi solicitud quede registrada y sepa cuántos días me quedan en el año

  Escenario: Solicitud válida se registra y descuenta solo días hábiles
    Dado que existe un empleado activo "Ana Torres" con fecha de ingreso "2024-01-10"
    Y no tiene vacaciones registradas en el año 2026
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10"
    Entonces la API responde 201
    Y "dias_habiles" es 5
    Y "dias_restantes" es 7

  Escenario: Se puede usar exactamente el saldo restante del año
    Dado que existe un empleado activo "Luis Marín" con fecha de ingreso "2023-05-02"
    Y ya tiene registrados 5 días hábiles de vacaciones en el año 2026
    Cuando solicita vacaciones del "2026-07-13" al "2026-07-21"
    Entonces la API responde 201
    Y "dias_habiles" es 7
    Y "dias_restantes" es 0

  Escenario: Los fines de semana y los festivos oficiales dentro del periodo no se descuentan
    Dado que existe un empleado activo "Carla Ibarra" con fecha de ingreso "2022-02-15"
    Y no tiene vacaciones registradas en el año 2026
    Cuando solicita vacaciones del "2026-12-21" al "2026-12-31"
    Entonces la API responde 201
    Y "dias_habiles" es 8
    Y "dias_restantes" es 4
    Y el mensaje de éxito es "Solicitud registrada: 8 días hábiles. Te quedan 4 días hábiles en 2026."

  Escenario: Error por antigüedad insuficiente
    Dado que existe un empleado activo "Pedro Nava" con fecha de ingreso "2025-12-21"
    Cuando solicita vacaciones del "2026-12-18" al "2026-12-20"
    Entonces la API responde 400
    Y el mensaje de error es "Se requiere al menos un año de antigüedad a la fecha de inicio"

  Escenario: Error cuando el periodo no incluye ningún día hábil
    Dado que existe un empleado activo "Miriam Solís" con fecha de ingreso "2020-01-05"
    Cuando solicita vacaciones del "2026-07-11" al "2026-07-12"
    Entonces la API responde 400
    Y el mensaje de error es "El periodo no incluye días hábiles"

  Escenario: Error cuando la solicitud rebasa los días disponibles del año
    Dado que existe un empleado activo "Jorge Campos" con fecha de ingreso "2019-03-01"
    Y ya tiene registrados 4 días hábiles de vacaciones en el año 2026
    Cuando solicita vacaciones del "2026-08-03" al "2026-08-13"
    Entonces la API responde 400
    Y el mensaje de error es "La solicitud excede los días disponibles: quedan 8 días hábiles"

  Escenario: Error cuando el empleado ya agotó su tope anual
    Dado que existe un empleado activo "Rosa Delgado" con fecha de ingreso "2018-06-20"
    Y ya tiene registrados 12 días hábiles de vacaciones en el año 2026
    Cuando solicita vacaciones del "2026-08-03" al "2026-08-04"
    Entonces la API responde 400
    Y el mensaje de error es "La solicitud excede los días disponibles: quedan 0 días hábiles"

  Escenario: Error cuando la fecha de fin es anterior a la fecha de inicio
    Dado que existe un empleado activo "Diego Ortiz" con fecha de ingreso "2021-04-11"
    Cuando solicita vacaciones del "2026-07-10" al "2026-07-05"
    Entonces la API responde 400
    Y el mensaje de error es "La fecha de fin no puede ser anterior a la fecha de inicio"

  Escenario: Error cuando el periodo cruza de un año a otro
    Dado que existe un empleado activo "Sofía Lara" con fecha de ingreso "2020-09-01"
    Cuando solicita vacaciones del "2026-12-28" al "2027-01-08"
    Entonces la API responde 400
    Y el mensaje de error es "Las vacaciones deben estar dentro de un mismo año calendario"

  Escenario: Error cuando el año de la solicitud no está en la tabla de festivos
    Dado que existe un empleado activo "Hugo Paredes" con fecha de ingreso "2018-01-01"
    Cuando solicita vacaciones del "2025-07-01" al "2025-07-05"
    Entonces la API responde 400
    Y el mensaje de error es "Solo se pueden solicitar vacaciones en 2026 y 2027"

  Escenario: Error cuando el empleado no existe
    Dado que no existe ningún empleado con id 9999
    Cuando se solicitan vacaciones del "2026-07-06" al "2026-07-10" para el empleado 9999
    Entonces la API responde 404
    Y el mensaje de error es "Empleado no encontrado"

  Escenario: Error cuando el empleado está dado de baja
    Dado que existe un empleado "Elena Ríos" con estado "baja"
    Cuando solicita vacaciones del "2026-07-06" al "2026-07-10"
    Entonces la API responde 409
    Y el mensaje de error es "No se pueden solicitar vacaciones para un empleado dado de baja"
