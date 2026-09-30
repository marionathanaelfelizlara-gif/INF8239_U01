# Diccionario de datos — `data/raw/dataset.csv`

| Columna | Significado | Tipo / Unidad | Fuente | Disponibilidad | Transformación aplicada | Riesgo / nota |
|---|---|---|---|---|---|---|
| `anio` | Año calendario de la denuncia | Entero (2018–2025) | Columna `AÑOS` en las 3 hojas del Excel original | Completa (0% ausentes) | Renombrada desde `AÑOS` | Ninguno |
| `mes` | Mes calendario de la denuncia | Texto (nombre del mes) | Columna `MESES` en las 3 hojas | Completa (0% ausentes) | Renombrada desde `MESES` | Ninguno |
| `provincia` | Provincia de la República Dominicana donde se registró la denuncia | Texto (categórico) | Columna `PROVINCIA`/`PROVINCIAS` (el nombre varía por hoja) | Completa (0% ausentes) | Renombrada y unificada entre hojas | Ninguno |
| `categoria_robo` | Categoría de origen del registro — **variable target** | Texto (3 clases: Automotor, Armas de Fuego, General) | Asignada por hoja de origen (no viene explícita en el Excel) | Completa (0% ausentes) | Columna agregada en `build_dataset_from_excel()` según la hoja de la que proviene cada fila | Es el target; no debe usarse ninguna variable derivada de esta como feature |
| `tipo_detalle` | Subtipo o clasificación específica dentro de la categoría | Texto (categórico) | `CLASIFICACIÓN DEL VEHÍCULO` (Automotor) / `TIPO DE ROBO` (General); no existe para Armas de Fuego | Parcial: ~16.3% ausente (1,061 de 6,516 filas, todas de Armas de Fuego, donde el dato no existe en la fuente) | Renombrada desde columnas con nombres distintos por hoja; `NA` explícito para Armas de Fuego | **Excluida de X en el modelado** (paso 7): sus valores son proxy casi perfecto de `categoria_robo` (fuga de información) |
| `cantidad_denuncias` | Número de denuncias reportadas para esa combinación año/mes/provincia/categoría | Entero (conteo) | `CANTIDAD DE DENUNCIAS POR ROBO DE VEHÍCULOS` / `ROBO ARMAS DE FUEGO` / `CANTIDAD DE DENUNCIAS POR ROBO DE GENERALES` | Completa (0% ausentes) | Renombrada y unificada entre hojas | Ninguno |

**Filas totales:** 6,516 (2,491 Automotor + 1,061 Armas de Fuego + 2,964 General). **Duplicados:** 0.
