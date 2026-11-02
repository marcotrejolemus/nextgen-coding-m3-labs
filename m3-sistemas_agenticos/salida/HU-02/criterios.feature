# language: es

Característica: Consultar el directorio de empleados
  Como persona del área de Recursos Humanos
  Quiero ver el directorio de empleados, buscarlos por nombre o correo y filtrarlos por departamento
  Para encontrar rápido a una persona

  Antecedentes:
    Dado que existen los siguientes empleados registrados
      | numero_empleado | nombre       | correo                    | puesto     | departamento      | estado |
      | EMP-0001        | Ana López    | ana.lopez@empresa.com     | Analista   | Tecnología        | activo |
      | EMP-0002        | Juan Pérez   | juan.perez@empresa.com    | Gerente    | Ventas            | activo |
      | EMP-0003        | Marta Ruiz   | marta.ruiz@empresa.com    | Contadora  | Finanzas          | baja   |

  Escenario: Camino feliz - ver el directorio completo
    Dado que estoy en la pantalla del directorio de empleados
    Cuando abro el directorio sin aplicar ningún filtro
    Entonces veo 3 empleados listados
    Y cada fila muestra número de empleado, nombre, puesto, departamento y estado
    Y veo la fila "EMP-0001 | Ana López | Analista | Tecnología | activo"
    Y veo la fila "EMP-0002 | Juan Pérez | Gerente | Ventas | activo"
    Y veo la fila "EMP-0003 | Marta Ruiz | Contadora | Finanzas | baja"

  Escenario: Buscar por nombre sin distinguir mayúsculas de minúsculas
    Dado que estoy en la pantalla del directorio de empleados
    Cuando busco por el texto "ANA LÓPEZ"
    Entonces veo 1 empleado listado
    Y veo la fila "EMP-0001 | Ana López | Analista | Tecnología | activo"

  Escenario: Buscar por correo sin distinguir mayúsculas de minúsculas
    Dado que estoy en la pantalla del directorio de empleados
    Cuando busco por el texto "JUAN.PEREZ@EMPRESA.COM"
    Entonces veo 1 empleado listado
    Y veo la fila "EMP-0002 | Juan Pérez | Gerente | Ventas | activo"

  Escenario: Filtrar por departamento
    Dado que estoy en la pantalla del directorio de empleados
    Cuando filtro por el departamento "Finanzas"
    Entonces veo 1 empleado listado
    Y veo la fila "EMP-0003 | Marta Ruiz | Contadora | Finanzas | baja"

  Escenario: Buscar un texto que no coincide con ningún empleado
    Dado que estoy en la pantalla del directorio de empleados
    Cuando busco por el texto "xyz-sin-coincidencias"
    Entonces veo el mensaje "No se encontraron resultados"
    Y no veo ninguna fila de empleado en la lista

  Escenario: Los empleados dados de baja siguen apareciendo en el directorio
    Dado que estoy en la pantalla del directorio de empleados
    Cuando abro el directorio sin aplicar ningún filtro
    Entonces veo a "Marta Ruiz" con estado "baja" en la lista
    Y su fila conserva número de empleado, nombre, puesto y departamento

# Preguntas abiertas
# - No se especifica el texto exacto del mensaje de "sin resultados"; se asumió "No se encontraron resultados".
# - No se especifica si la búsqueda también incluye coincidencias por puesto o número de empleado, además de nombre y correo.
# - No se especifica si existe paginación ni el orden por defecto de la lista (se asumió orden de alta, sin ordenar explícitamente).
# - No se especifica si se puede filtrar por estado (activo/baja) además de por departamento.
