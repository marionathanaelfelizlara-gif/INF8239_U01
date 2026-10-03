# Ficha del dataset

- **Dominio:** Seguridad ciudadana / criminalidad — estadísticas de denuncias de robo en República Dominicana.
- **Unidad de análisis:** Un registro mensual de denuncias, desagregado por año, mes, provincia y categoría de robo (Automotor, Armas de Fuego, General).
- **Decisión que apoyaría este modelo:** Clasificar automáticamente un registro de denuncia según su categoría a partir de variables estructurales (año, mes, provincia, cantidad de denuncias), útil para detectar inconsistencias de registro o para automatizar el etiquetado de reportes nuevos que publique el MIP.
- **Target tentativo:** `categoria_robo` (Automotor / Armas de Fuego / General).
- **Tipo de tarea:** Clasificación multiclase (3 clases).
- **Error más costoso:** Confundir un registro de **Armas de Fuego** con otra categoría — este tipo de robo tiene mayor severidad y prioridad de intervención policial, así que un falso negativo aquí (predecir otra categoría cuando en realidad es Armas de Fuego) es más costoso que un error entre Automotor y General.
- **Usuario de la solución:** Analistas del Ministerio de Interior y Policía (MIP) o de un observatorio de seguridad ciudadana, para monitorear tendencias por provincia/periodo y asegurar consistencia en el registro de denuncias.

## Comparación de candidatos

| Criterio | Candidato A — Turismo Cultural | Candidato B — Robos (elegido) |
|---|---|---|
| **Procedencia** | Ministerio de Turismo (MITUR), Depto. de Turismo Cultural | Ministerio de Interior y Policía (MIP) |
| **URL ficha** | [datos.gob.do/dataset/turismo-cultural](https://datos.gob.do/dataset/turismo-cultural) | [datos.gob.do/dataset/estadisticas-de-robos-...](https://datos.gob.do/dataset/estadisticas-de-robos-de-automotores-armas-de-fuego-y-denuncias-de-robos) |
| **Licencia** | ODbL (Open Database License) | ODbL (Open Database License) |
| **Cobertura temporal** | 2018–2026 | 2018–2025 |
| **Formatos disponibles** | CSV, ODS, XLSX | XLSX, CSV, ODS |
| **Filas/columnas** | No evaluado a fondo — organizado por producto/indicador/mes, sin descarga ni carga completa del archivo | 6,516 filas × 6 columnas (tras unificar las 3 hojas del Excel) |
| **Target y clases** | No hay una variable de clasificación clara y predefinida; son series de indicadores turísticos, más apto para análisis descriptivo/series de tiempo que para clasificación | `categoria_robo`, 3 clases (Automotor, Armas de Fuego, General) |
| **Ausentes** | No evaluado | `tipo_detalle`: 16.3% ausente (1,061 de 6,516 filas); resto de columnas completas |
| **Riesgo de fuga** | No evaluado | Alto en `tipo_detalle` (proxy casi perfecto del target) — se excluye del modelo |

**Motivo de la decisión:** se descartó el Candidato A porque no ofrece una variable objetivo de clasificación clara y verificable con al menos dos clases (requisito del paso 3 del manual), mientras que el Candidato B sí la tiene de forma natural (`categoria_robo`, derivado de la hoja de origen de cada fila).

**Estado de aprobación docente:** _pendiente de confirmar por el estudiante antes de la entrega final._

## Procedencia y licencia (Candidato B — elegido)

- **Fuente:** Ministerio de Interior y Policía (MIP), República Dominicana.
- **Publicado en:** [datos.gob.do](https://datos.gob.do/dataset/estadisticas-de-robos-de-automotores-armas-de-fuego-y-denuncias-de-robos)
- **Licencia:** ODbL (Open Database License).
- **Cobertura temporal:** 2018–2025.
- **Formato original:** Excel (`.xlsx`) con 3 hojas de esquemas distintos: `ROBOS_AUTOMOTOR`, `ROBOS_ARMAS_FUEGO`, `ROBOS_GENERALES`.

## Justificación de columna retirada (fuga de información)

Ver el paso 7 del notebook `notebooks/02_dataset_publico.ipynb`: la columna `tipo_detalle` se excluye de las variables predictoras porque sus valores son subtipos que existen únicamente dentro de una sola categoría (proxy casi perfecto del target), no por motivos de métrica.
