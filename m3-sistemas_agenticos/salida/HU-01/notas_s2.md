# Módulo 3 — Laboratorio 2: Diseño de flujos complejos

**Historia de usuario:** HU-01 — Registrar empleado
**Fecha de ejecución:** 30 de octubre de 2026
**Estado:** Aplicación generada y validada manualmente; verificación determinista ejecutada exitosamente después de corregir una incompatibilidad con npm en Windows.

## 1. Lab 2A — Lectura del grafo

Se revisó `flujos/flujo_s2.py` y se identificaron los nodos principales: `analizar`, `pedir_aclaracion`, `disenar_casos`, `planificar`, `aprobar_plan`, `construir`, `verificar` y `fin`. Se identificaron decisiones condicionales y el punto de aprobación humana mediante `interrupt()` y `Command(resume=...)`.

**Evidencia de grafo:** revisar `flujos/salidas/grafo_flujo_s2.html` y compararlo con el dibujo personal del flujo. La existencia de un dibujo manual y su comparación final quedan pendientes de confirmar.

## 2. Lab 2B — Comentarios al plan y aprobación humana

**Primer comentario de rechazo:**

> No apruebo el plan todavía. Incluye pruebas automatizadas para POST /api/empleados que validen los códigos HTTP 201, 409 y 422, correo duplicado sin distinguir mayúsculas, campos obligatorios vacíos y fecha de ingreso futura. Define un formato de error consistente entre FastAPI y React, y utiliza únicamente los departamentos establecidos en la historia de usuario. Presenta el plan revisado antes de generar código.

**¿Incorporó el segundo plan el comentario?** Parcialmente. El desarrollador respetó la separación de responsabilidades: la escritura de pruebas automatizadas pertenece al Agente 5. Agregó manejo homogéneo de errores y el catálogo de departamentos, pero propuso leer `err.response.data.detail`, expresión de Axios no compatible con la propuesta basada en `fetch` nativo.

**Segundo comentario de rechazo:**

> El plan está casi listo, pero antes de aprobarlo corrige el contrato frontend/backend: utiliza fetch nativo y procesa los errores mediante response.ok, await response.json() y data.detail; no uses err.response.data.detail, que corresponde a Axios. Mantén los mensajes 409 y 422 de las reglas de negocio, los data-testid del directorio y las pruebas automatizadas reservadas al Agente 5. Presenta el plan final sin generar código todavía.

**Resultado:** El tercer plan aclaró el uso de `fetch` y `response.ok` y fue aprobado. Claude Code construyó el backend FastAPI/SQLAlchemy/SQLite y el frontend React/Vite.

## 3. Lab 2C — Tabla de verificación manual

| Criterio / comprobación | Resultado | Evidencia |
| --- | --- | --- |
| `GET /api/salud` | Cumplido | HTTP 200 |
| `GET /api/departamentos` | Cumplido | HTTP 200 |
| Registro con datos válidos | Cumplido | `POST /api/empleados` → HTTP 201 |
| Número de empleado asignado por el sistema | Cumplido | Mensaje `Empleado registrado con número EMP-0002` |
| Confirmación visual tras guardar | Cumplido | React mostró el identificador generado |
| Correo duplicado sin distinguir mayúsculas | Cumplido | HTTP 409; `El correo ya está registrado` |
| Correo ajeno a `@empresa.com` | Cumplido | HTTP 422; `Usa el correo corporativo @empresa.com` |
| Fecha de ingreso futura | Cumplido | HTTP 422; `La fecha de ingreso no puede ser futura` |
| Limpieza del formulario después del éxito | Cumplido | Campos vacíos en la captura posterior al registro |
| Revisión completa de todos los `data-testid` | No verificado completamente | Pendiente de comparar el DOM con las convenciones |
| Ejecución de los casos de prueba automatizados | Pendiente de la sesión 3 | No equivale a las pruebas manuales realizadas |

## 4. Verificación determinista y diagnóstico de Windows

La ejecución inicial de `flujos.flujo_s2` finalizó con `FileNotFoundError: [WinError 2]` durante `subprocess.run(["npm", "install"/...])`. El proceso concluyó con una excepción antes de imprimir la bitácora final `app LISTA`. Los archivos generados no se perdieron.

Se corrigió exclusivamente la infraestructura `flujos/verificacion.py` para llamar a `npm.cmd` desde Windows. Después se ejecutó por separado `verificar_app()` con el resultado:

```text
VERIFICACION: OK
## Backend
http://127.0.0.1:8010/api/salud -> 200
## Frontend
vite v5.4.21 building for production...
31 modules transformed
built in 379ms
```

La validación manual también comprobó FastAPI en el puerto 8000 y React en el 5173. **La prueba posterior fue satisfactoria, aunque no recuperó la bitácora final de la ejecución original de LangGraph.**

## 5. Costos reportados

| Etapa | Costo USD |
| --- | ---: |
| Primer plan del desarrollador | 0.16 |
| Segundo plan del desarrollador | 0.06 |
| Tercer plan del desarrollador | 0.08 |
| Construcción por Claude Code, 61 turnos | 1.32 |
| **Subtotal confirmado por la traza** | **1.62** |

El subtotal no incluye costos no informados del Analista o Diseñador. No existe una cifra final consolidada de la bitácora `app LISTA`, ya que el proceso original falló durante la verificación.

## 6. Patrones identificados y preguntas de reflexión

**Encadenamiento:** `analizar → disenar_casos → planificar → aprobar_plan → construir → verificar` coordina dependencias consecutivas.

**Enrutamiento condicional:** las funciones `despues_de_analizar`, `despues_de_aclarar`, `despues_de_aprobar` y `despues_de_verificar` deciden el siguiente nodo a partir del estado y de las verificaciones.

**Human-in-the-Loop:** `aprobar_plan` pausa mediante `interrupt()` y reanuda con `Command(resume=...)`; sin ese nodo, el agente podría escribir código sin consentimiento sobre el plan.

**Evaluador-optimizador:** si la verificación determinista falla, el flujo puede regresar a `construir`, dentro de un límite de intentos. Sin una verificación en código, la declaración del agente no bastaría para afirmar que la aplicación funciona.

**¿Qué información necesitaba para aprobar el plan?** Contratos de error coherentes entre backend y frontend, respeto a las reglas de negocio y claridad sobre la responsabilidad de automatizar pruebas.

**¿Aprobar después de cada nodo?** Aumentaría el control, pero introduciría interrupciones innecesarias y retrasaría el flujo. Resulta preferible reservar las aprobaciones para decisiones con impacto relevante.

## 7. Pendientes y preparación para la sesión 3

- [ ] Comprobar y conservar el grafo `flujos/salidas/grafo_flujo_s2.html`.
- [ ] Verificar que todos los selectores `data-testid` requeridos estén presentes.
- [ ] Revisar que las notas reflejen las evidencias personales de la práctica.
- [ ] Hacer un commit controlado, sin incluir `.env`, bases de datos de prueba, `node_modules`, `dist/` ni secretos.
- [ ] Continuar con HU-02 y la sesión 3 después del commit.
