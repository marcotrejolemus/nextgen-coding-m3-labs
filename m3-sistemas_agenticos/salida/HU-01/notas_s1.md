# Módulo 3 — Laboratorio 1: Arquitectura de agentes

**Estudiante:** Marco Antonio Trejo Lemus
**Programa:** Next-Gen Coding — Desarrollo de Software con IA Generativa
**Institución:** Tecnológico de Monterrey
**Historia de usuario:** HU-01 — Registrar empleado
**Fecha de ejecución:** 30 de octubre de 2026
**Estado:** Completado y registrado en Git (commit fadff0c).

## 1. Evidencias

- **Lab 1A — Agente y control de permisos.** Se comprobó que las herramientas de archivos respetan las rutas permitidas: un intento de lectura de `secretos_demo.txt` fuera de las rutas autorizadas produjo `PermissionError` y la prueba imprimió `PASS: Acceso denegado correctamente`.
- **Lab 1B — Analista.** Se ejecutó el analista sobre `historias/HU-01-registrar-empleado.md` y se generó `salida/HU-01/criterios.feature`. Fue necesario un segundo intento para superar las validaciones.
- **Lab 1C — Diseñador de pruebas.** Se ejecutó el diseñador sobre los criterios y se produjo `salida/HU-01/casos_prueba.json`, validado como JSON. El ejercicio individual reportó **18 casos** (9 de API y 9 E2E). La cantidad puede variar al regenerar el archivo en otros laboratorios.

## 2. ¿Por qué ocurrió `PermissionError` en el Lab 1A?

La herramienta intentó acceder a una ruta fuera de las carpetas de lectura explícitamente autorizadas. El control de permisos del agente rechazó la operación. Esto demuestra que el agente no puede ampliar su acceso al sistema de archivos por iniciativa propia.

## 3. ¿Qué corrigió el validador?

El primer intento del analista no satisfizo todas las verificaciones de los criterios Gherkin. La generación requirió un segundo intento antes de obtener el archivo aceptado. **Pendiente:** recuperar de la bitácora original el mensaje exacto del validador y describir qué condición específica corrigió; no debe inferirse sin revisar esa salida.

## 4. ¿Cuántos pasos utilizó cada agente?

| Agente | Dato confirmado | Dato pendiente |
| --- | --- | --- |
| Analista | Dos intentos en el Lab 1B | Número exacto de pasos/herramientas de cada intento según su traza original |
| Diseñador de pruebas | Un intento en el Lab 1C | Número exacto de pasos/herramientas según su traza original |

> Los intentos de generación no son necesariamente iguales al número de pasos internos del agente. Se conserva esta distinción hasta recuperar las trazas.

## 5. ¿Qué cambiaría en las instrucciones de los agentes?

- **Analista:** pedir que todos los escenarios estén expresados en Gherkin válido y vinculados a reglas de negocio concretas, evitando supuestos no documentados.
- **Diseñador:** exigir trazabilidad entre escenario Gherkin, identificador del caso de prueba, nivel API/E2E y `data-testid` esperado.
- **Herramientas:** conservar rutas de lectura y escritura restringidas y denegar explícitamente los accesos fuera de alcance.

## 6. Reflexión

El flujo combina decisiones del modelo con controles deterministas. El agente propone contenido y usa herramientas; el validador decide si un resultado puede aceptarse. La validación reduce el riesgo de que una respuesta aparentemente correcta incumpla los contratos del proyecto.

## 7. Pendientes antes del commit

- [ ] Revisar que `criterios.feature` y `casos_prueba.json` estén presentes y actualizados.
- [ ] Completar el error exacto corregido por el validador, si se conserva la traza.
- [ ] Completar el número exacto de pasos internos, si se conserva la traza.
- [ ] Revisar y guardar las notas con interpretación personal.
