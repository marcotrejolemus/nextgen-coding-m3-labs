# Laboratorio 4A - HU-03
## Intervencion humana y analisis de causa raiz

### Objetivo
Implementar y validar la edicion y baja de empleados mediante
una fabrica multiagente con supervision humana.

### Resultado original del flujo
- Estado: ESCALAR A UNA PERSONA.
- Ciclos de correccion: 2.
- Pruebas iniciales: 23 fallidas por errores de conexion.
- Responsable identificado por triage: despliegue.

### Incidente 1: conectividad Docker/WSL2
Sintomas:
- Errores WinError 10053 y 10054.
- Backend y Nginx respondian internamente.
- Windows no lograba acceder consistentemente a los puertos.
- WSL2 presento el error WSAENOBUFS.
- Se identifico un proceso Uvicorn local adicional en el puerto 8000.

Acciones:
- Diagnostico de procesos, puertos y contenedores.
- Finalizacion controlada del servidor Uvicorn local.
- Reinicio de Windows y posterior inicio de Docker Desktop.

Resultado:
- HTTP 200 en localhost:8000/api/salud.
- HTTP 200 en localhost:8080/api/salud.
- HTTP 200 en la pagina principal de React.

La conectividad se recupero despues del reinicio.
No se determino de manera concluyente la causa interna
del fallo de WSL2.

### Incidente 2: mensajes de confirmacion React
Sintomas:
- API HU-03: 6 pruebas aprobadas.
- E2E HU-03: 3 aprobadas y 2 fallidas.
- CP-02 y CP-04 no encontraban mensaje-exito.

Causa raiz:
App.jsx cerraba el formulario despues de guardar.
El mensaje de exito estaba almacenado en el componente
que React desmontaba inmediatamente.

Correccion:
Se traslado el manejo del mensaje de confirmacion al
componente padre App.jsx, conservando el refresco automatico
del directorio y los selectores data-testid.

### Verificacion final
- API HU-03: 6/6 aprobadas.
- E2E HU-03: 5/5 aprobadas.
- Regresion completa: 23/23 aprobadas.
- Ultima suite: 23 passed in 13.20s.

### Aprendizajes
- La salud interna de un contenedor no garantiza conectividad externa.
- El triage puede identificar un responsable sin resolver el problema.
- El ciclo de vida de los componentes React afecta las pruebas E2E.
- La supervision humana complementa la automatizacion.
- Las pruebas de regresion son indispensables antes del commit.

### Conclusion
HU-03 fue validada satisfactoriamente despues de una
intervencion humana. Se conserva el reporte original de
escalamiento como evidencia del funcionamiento del flujo.
