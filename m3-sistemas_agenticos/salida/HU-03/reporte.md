# Reporte · HU-03

**Estado:** ESCALAR A UNA PERSONA
**Costo de agentes:** 4.92 USD
**Ciclos de corrección:** 2

## Bitácora
- Filtro de historia: OK
- Criterios escritos en criterios.feature
- Preguntas abiertas: la persona respondió 'si'
- Casos de prueba escritos en casos_prueba.json
- Plan rechazado: Por favor, revisa el plan para preservar todas las funcionalidades, validaciones y selectores de prueba existentes de HU-01 y HU-02. Evita duplicar los atributos data-testid entre los formularios de registro y edición cuando estén visibles simultáneamente. Utiliza consistentemente empleado.id (numérico) para identificar filas y acciones, sin confundirlo con numero_empleado (EMP-000x). Define explícitamente el comportamiento para empleados inexistentes (404), empleados dados de baja que intenten editarse (409), solicitudes de baja repetidas y fechas de baja inválidas (422). Conserva el comportamiento esperado en CP-05 para los campos inmutables, salvo que se revisen de manera consistente los criterios de aceptación y los casos de prueba. Actualiza automáticamente el directorio después de editar o dar de baja a un empleado, sin recargar la página. No introduzcas dependencias ni cambios ajenos a HU-03.
- Plan aprobado por una persona
- Construcción 1
- Verificación: OK
- Pruebas automatizadas: OK (11 casos)
- Despliegue: FALLA
- Despliegue y pruebas listos
- Pruebas E2E: 23 failed in 17.08s
- Triage → despliegue: Todas las pruebas (API y E2E, de distintas historias de usuario) fallan con errores de conexión a nivel de transporte (ReadError/WinError 10054 y 10053: conexión cerrada/abortada por el host remoto), no con fallos de aserción sobre el comportamiento de la aplicación. Esto indica que el servidor/contenedor de la aplicación no está respondiendo o se cayó durante las pruebas, en lugar de un error funcional o de la prueba en sí.
- Despliegue corregido
- Pruebas E2E: 23 failed in 9.72s
- Triage → despliegue: Todas las pruebas (API y E2E) fallan con errores de conexión (ReadError, WinError 10054/10053 - conexión cerrada/abortada por el host remoto) en lugar de errores de aserción sobre el contenido de las respuestas. Esto indica que el servidor de la aplicación no está disponible, se cayó durante la ejecución, o el contenedor/proceso backend no está respondiendo, en vez de un fallo funcional de la lógica de negocio o de la prueba.
- Despliegue corregido
- Pruebas E2E: 23 failed in 9.90s

## Última ejecución de pruebas
```
23 failed in 9.90s
- tests.api.test_hu_02::test_cp_01_ver_directorio_completo
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_02::test_cp_03_buscar_por_nombre_sin_distinguir_mayusculas
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_02::test_cp_05_buscar_por_correo_sin_distinguir_mayusculas
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_02::test_cp_07_filtrar_por_departamento
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_02::test_cp_09_buscar_texto_sin_coincidencias
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_02::test_cp_11_empleados_baja_aparecen_en_directorio
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_03::test_cp_01_editar_puesto_y_departamento
  httpx.ReadError: [WinError 10053] An established connection was aborted by the software in your host machine
- tests.api.test_hu_03::test_cp_03_dar_de_baja_empleado_activo
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_03::test_cp_05_no_editar_numero_empleado_ni_correo
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_03::test_cp_06_error_al_editar_empleado_dado_de_baja
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_03::test_cp_08_error_al_editar_con_departamento_no_permitido
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.api.test_hu_03::test_cp_10_error_fecha_baja_anterior_a_fecha_ingreso
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_02_e2e::test_cp_02_ver_directorio_completo[chromium]
  httpx.ReadError: [WinError 10053] An established connection was aborted by the software in your host machine
- tests.e2e.test_hu_02_e2e::test_cp_04_buscar_por_nombre_sin_distinguir_mayusculas[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_02_e2e::test_cp_06_buscar_por_correo_sin_distinguir_mayusculas[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_02_e2e::test_cp_08_filtrar_por_departamento[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_02_e2e::test_cp_10_buscar_texto_sin_coincidencias[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_02_e2e::test_cp_12_empleados_baja_aparecen_en_directorio[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_03_e2e::test_cp_02_editar_puesto_y_departamento[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_03_e2e::test_cp_04_dar_de_baja_empleado_activo[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_03_e2e::test_cp_07_error_al_editar_empleado_dado_de_baja[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_03_e2e::test_cp_09_error_al_editar_con_departamento_no_permitido[chromium]
  httpx.ReadError: [WinError 10054] An existing connection was forcibly closed by the remote host
- tests.e2e.test_hu_03_e2e::test_cp_11_error_fecha_baja_anterior_a_fecha_ingreso[chromium]
  httpx.ReadError: [WinError 10053] An established connection was aborted by the software in your host machine
```