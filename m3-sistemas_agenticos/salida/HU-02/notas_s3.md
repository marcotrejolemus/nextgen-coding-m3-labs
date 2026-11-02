# Laboratorio 3 — Sistemas Multiagente

**Estudiante:** Marco Antonio Trejo Lemus
**Programa:** Next-Gen Coding — Desarrollo de Software con IA Generativa
**Institución:** Tecnológico de Monterrey
**Historia de usuario:** HU-02 — Consultar directorio de empleados
**Fecha de documentación:** 2 de noviembre de 2026

## 1. Objetivo

Extender la aplicación HU-01 mediante la implementación de HU-02, utilizando una fábrica de software multiagente coordinada por LangGraph, incorporando despliegue con Docker Compose y automatización de pruebas mediante pytest y Playwright.

## 2. Arquitectura multiagente

La fábrica coordinó cinco agentes especializados:

1. **Analista:** generó seis escenarios de aceptación en Gherkin.
2. **Diseñador de pruebas:** generó doce casos de prueba, seis API y seis E2E.
3. **Desarrollador:** implementó el directorio de empleados conservando la funcionalidad de HU-01.
4. **Despliegue:** creó los artefactos Docker necesarios y levantó los servicios.
5. **Automatizador:** generó pruebas automatizadas con pytest y Playwright.

Los agentes 4 y 5 se ejecutaron en ramas paralelas de LangGraph, sincronizadas posteriormente en el nodo `listo`.

## 3. Supervisión humana

El primer plan fue rechazado para solicitar mejoras en:

- Conservación de las validaciones y funcionalidad existente de HU-01.
- Actualización automática del directorio después de registrar empleados.
- Manejo de errores y estados de carga de la API.
- Uso de `fetch` y `response.ok`.
- Respeto a los contratos y selectores `data-testid`.

El segundo plan incorporó estas observaciones y fue aprobado antes de iniciar la construcción.

## 4. Resultado del despliegue Docker

Se construyeron imágenes para backend y frontend y se iniciaron los servicios mediante Docker Compose.

Resultado observado de `docker compose ps`:

| Contenedor | Servicio | Estado | Puerto |
|---|---|---|---|
| `app-backend-1` | backend | Up (healthy) | 8000 |
| `app-frontend-1` | frontend | Up | 8080 |

La aplicación se visualizó correctamente en `http://localhost:8080`, mostrando el formulario de registro de HU-01 y el directorio de HU-02.

## 5. Resultados de pruebas automatizadas

| Validación | Resultado |
|---|---|
| Pruebas API | 6 aprobadas en 3.87 s |
| Pruebas E2E con Chromium | 6 aprobadas en 42.71 s |
| Suite completa `pytest app/tests -q` | **12 aprobadas en 35.79 s** |

Durante la primera ejecución E2E se identificó una dependencia faltante: el navegador Chromium requerido por Playwright.

Se resolvió mediante:

`python -m playwright install chromium`

Después de la instalación, todas las pruebas E2E se ejecutaron satisfactoriamente.

## 6. Auditoría de operaciones

El archivo `auditoria.jsonl` registró 145 eventos:

| Rol | Eventos |
|---|---:|
| Desarrollador | 79 |
| Automatizador | 33 |
| Planificación | 17 |
| Despliegue | 16 |
| **Total** | **145** |

Se registraron operaciones de lectura, escritura, edición y ejecución de comandos.

**Intentos denegados:** No se confirmó un evento específico de denegación con la evidencia revisada. El formato actual de auditoría conserva información de las solicitudes a herramientas, pero no registra explícitamente la decisión de autorización. Queda pendiente contrastar las trazas de ejecución para identificar una denegación comprobable.

**Observación para la sesión 4:** revisar la cobertura de los hooks de seguridad respecto a las llamadas registradas a la herramienta `PowerShell`.

## 7. Costos de ejecución

El flujo HU-02 reportó un costo total de **USD 1.56**.

Este importe corresponde al costo informado por el proceso multiagente y no representa una evaluación de costos de infraestructura o producción.

## 8. Reflexiones académicas

**¿Qué topología tiene la fábrica?**

Un flujo de orquestación determinista mediante LangGraph, que combina etapas secuenciales, decisiones humanas, validaciones automáticas y ramas paralelas.

**¿Por qué despliegue y automatización pueden ejecutarse simultáneamente?**

Porque ambos utilizan la aplicación ya construida, pero realizan tareas distintas. El automatizador escribe pruebas mientras el agente de despliegue prepara los contenedores. La ejecución posterior de pruebas E2E sí requiere que los servicios estén disponibles.

**¿Qué cambiaría si existieran quince agentes?**

Evaluaría una arquitectura jerárquica o supervisada para organizar grupos especializados y reducir la complejidad del grafo principal. La decisión dependería de la necesidad de coordinación dinámica, trazabilidad, costos y tolerancia a fallos.

## 9. Conclusión

El Laboratorio 3 demostró el funcionamiento práctico de una fábrica multiagente capaz de analizar requisitos, generar código, desplegar una aplicación y producir pruebas automatizadas.

La aplicación HU-02 se ejecutó correctamente en Docker y superó las doce pruebas de su suite automatizada.

El principal aprendizaje fue comprender la colaboración entre agentes especializados, la importancia de la supervisión humana, la verificación determinista y la necesidad de contar con mecanismos de auditoría y control de permisos.

**Resultado:** Laboratorio 3B y validaciones funcionales de 3C completados satisfactoriamente. Documentación de denegaciones pendiente de evidencia adicional.