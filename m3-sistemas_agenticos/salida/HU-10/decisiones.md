# Decisiones técnicas — HU-10: Solicitar vacaciones

**1. ¿Qué pasos son workflow y cuáles son agentes?**

La fábrica combina un workflow determinista orquestado con LangGraph y seis agentes especializados. El workflow controla el orden de ejecución, las validaciones, las transiciones y los reintentos. Los agentes realizan tareas que requieren razonamiento y uso de herramientas: analizar requisitos, diseñar pruebas, desarrollar, desplegar, automatizar y diagnosticar fallos. En HU-10, el analista generó 12 escenarios y el diseñador produjo 22 casos.

**2. ¿Cómo se validaron las salidas estructuradas?**

El analista utilizó validaciones de estructura Gherkin. El diseñador empleó esquemas Pydantic, comprobación de cobertura por escenario e identificadores únicos. La aplicación pasó las verificaciones del backend y la compilación del frontend. Finalmente, la suite automatizada reportó 45 pruebas aprobadas, todas aprobadas. Los validadores no reportaron errores durante esta ejecución; la cobertura de reglas se reforzó mediante instrucciones y revisión humana.

**3. ¿Dónde intervine como persona?**

Intervine durante la aprobación del plan del desarrollador. Solicité reforzar el cálculo inclusivo de días hábiles, los festivos, el aniversario del 29 de febrero, el límite anual, la persistencia SQLite y la compatibilidad con HU-01 a HU-03. Mis observaciones multilínea fueron procesadas como varios rechazos individuales, ocasionando replanificaciones adicionales. Finalmente revisé y aprobé el plan antes de autorizar la construcción.

**4. ¿Qué arquitectura utilizó la fábrica y por qué?**

Se utilizó LangGraph con un grafo de estados y transiciones condicionales. Esta arquitectura permite combinar una secuencia controlada, aprobación Human-in-the-Loop y ejecución paralela de despliegue y automatización. Es preferible aquí a una coordinación completamente autónoma porque las etapas son conocidas y requieren trazabilidad, validaciones y control del costo.

**5. ¿Qué falló y cómo se resolvió?**

No se necesitaron ciclos automáticos de corrección del código en HU-10. El principal inconveniente ocurrió durante la revisión humana: las observaciones fueron ingresadas como respuestas separadas, generando múltiples planes. La fábrica continuó hasta recibir la aprobación explícita. Su resultado final fue **LISTA**, con cero ciclos de corrección y 45 pruebas aprobadas. Se mantuvieron las defensas de seguridad y se conservó `auditoria.jsonl` como evidencia de ejecución.