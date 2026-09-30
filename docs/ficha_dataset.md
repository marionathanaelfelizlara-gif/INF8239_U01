# Ficha del dataset

- **Dominio:** Seguridad ciudadana / criminalidad — estadísticas de denuncias de robo en República Dominicana.
- **Unidad de análisis:** Un registro mensual de denuncias, desagregado por año, mes, provincia y categoría de robo (Automotor, Armas de Fuego, General).
- **Decisión que apoyaría este modelo:** Clasificar automáticamente un registro de denuncia según su categoría a partir de variables estructurales (año, mes, provincia, cantidad de denuncias), útil para detectar inconsistencias de registro o para automatizar el etiquetado de reportes nuevos que publique el MIP.
- **Target tentativo:** `categoria_robo` (Automotor / Armas de Fuego / General).
- **Tipo de tarea:** Clasificación multiclase (3 clases).
- **Error más costoso:** Confundir un registro de **Armas de Fuego** con otra categoría — este tipo de robo tiene mayor severidad y prioridad de intervención policial, así que un falso negativo aquí (predecir otra categoría cuando en realidad es Armas de Fuego) es más costoso que un error entre Automotor y General.
- **Usuario de la solución:** Analistas del Ministerio de Interior y Policía (MIP) o de un observatorio de seguridad ciudadana, para monitorear tendencias por provincia/periodo y asegurar consistencia en el registro de denuncias.

## Procedencia y licencia

- **Fuente:** Ministerio de Interior y Policía (MIP), República Dominicana.
- **Publicado en:** [datos.gob.do](https://datos.gob.do/dataset/estadisticas-de-robos-de-automotores-armas-de-fuego-y-denuncias-de-robos)
- **Licencia:** ODbL (Open Database License).
- **Cobertura temporal:** 2018–2025.
- **Formato original:** Excel (`.xlsx`) con 3 hojas de esquemas distintos: `ROBOS_AUTOMOTOR`, `ROBOS_ARMAS_FUEGO`, `ROBOS_GENERALES`.
- **Candidato alternativo considerado:** Turismo Cultural (MITUR) — descartado en favor de este dataset porque ofrece un target de clasificación multiclase más claro (categoria_robo) y una pregunta de negocio más concreta.

## Justificación de columna retirada (fuga de información)

Ver el paso 7 del notebook `notebooks/02_dataset_publico.ipynb`: la columna `tipo_detalle` se excluye de las variables predictoras porque sus valores son subtipos que existen únicamente dentro de una sola categoría (proxy casi perfecto del target), no por motivos de métrica.
