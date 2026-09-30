# INF-8239 · Ciencia de Datos II — Unidad 01

Proyecto de laboratorios guiados: LAB00 (entorno), LAB01 (SVM con dataset de referencia) y LAB02 (búsqueda, selección y auditoría de un dataset público).

## Instalación

```
python -m venv .venv
.venv\Scripts\activate
pip install -r Requirements.txt
```

Para ejecutar notebooks y pruebas necesitas el kernel/entorno `.venv` seleccionado (no el Python global del sistema).

## LAB02 — Dataset público

**Dataset elegido:** Estadísticas de Robos de Automotores, Armas de Fuego y Denuncias de Robos (Ministerio de Interior y Policía, vía [datos.gob.do](https://datos.gob.do/dataset/estadisticas-de-robos-de-automotores-armas-de-fuego-y-denuncias-de-robos), licencia ODbL). Ver detalle completo de procedencia y justificación en [`docs/ficha_dataset.md`](docs/ficha_dataset.md) y el diccionario de columnas en [`docs/diccionario_datos.md`](docs/diccionario_datos.md).

### Descarga / construcción del dataset

El archivo fuente (`data/raw/robos-automotor-armas-de-fuego-y-denuncias-de-robo-2018-2025.xlsx`) sí está versionado en este repositorio (ver `.gitignore`), porque no se usa una URL de descarga reproducible sino el archivo Excel oficial con sus 3 hojas. Para regenerar `data/raw/dataset.csv` a partir de él:

```python
from inf8239_u01.data import build_dataset_from_excel
build_dataset_from_excel("data/raw/robos-automotor-armas-de-fuego-y-denuncias-de-robo-2018-2025.xlsx")
```

Esto ya está automatizado en la primera celda de código de `notebooks/02_dataset_publico.ipynb`.

### Target y métrica

- **Target:** `categoria_robo` (3 clases: Automotor, Armas de Fuego, General).
- **Métrica:** F1-macro (da igual peso a las 3 clases, relevante porque Armas de Fuego es la clase minoritaria y la de error más costoso).
- **Columna excluida de X:** `tipo_detalle`, por fuga de información (ver justificación en `docs/ficha_dataset.md` y en el paso 7 del notebook).

### Ejecución

Notebook completo: `notebooks/02_dataset_publico.ipynb` (correr con el kernel `.venv`, "Run All").

Pruebas:

```
set PYTHONPATH=src
python -m pytest -q
```

> **Nota:** el paso 9 del notebook (entrenamiento SVM vs. baseline) requiere aprobación previa del docente sobre el dataset elegido antes de ejecutarse como resultado final.

## Estructura del repositorio

```
data/raw/       Dataset fuente (.xlsx) y generado (dataset.csv, no versionado)
docs/           Ficha del dataset y diccionario de datos
notebooks/      Notebooks guiados de cada laboratorio
reports/        Resultados guardados (cv_results, modelos .joblib)
src/            Código fuente reutilizable (paquete inf8239_u01)
tests/          Pruebas automatizadas (pytest)
```

## Conclusión

Este laboratorio partió de una decisión temprana: elegir entre dos datasets públicos dominicanos (Turismo Cultural del MITUR y Estadísticas de Robos del MIP) evaluando cuál ofrecía una pregunta de clasificación más clara y una unidad de análisis más manejable. Se optó por el dataset de robos porque su variable de origen (la hoja del Excel de la que proviene cada fila) se presta naturalmente a un target de clasificación multiclase de 3 categorías, con una decisión de negocio concreta detrás: ayudar a un analista del MIP a verificar la consistencia del registro de denuncias.

El archivo fuente llegó dividido en 3 hojas con esquemas de columnas distintos entre sí, y sin una URL de descarga directa reutilizable como la que asume el flujo estándar del manual. Esto llevó a construir una función propia (`build_dataset_from_excel`) que unifica las 3 hojas en un solo dataset tabular, documentando explícitamente el origen de cada fila mediante la columna `categoria_robo`. Se decidió versionar el Excel original en el repositorio (en vez de solo el CSV derivado) precisamente para que el proyecto sea reproducible por cualquier persona que lo clone, sin depender de una descarga externa.

La auditoría del dataset combinado (6,516 filas, sin duplicados) reveló un solo patrón de ausentes relevante: la columna `tipo_detalle` está vacía en el 16.3% de las filas, correspondientes exactamente a los registros de Armas de Fuego, categoría para la cual esa subclasificación no existe en la fuente original. Al examinar esta columna con más detalle se detectó algo más importante que la simple ausencia de datos: sus valores no ausentes son subtipos que solo aparecen dentro de una única categoría del target, lo que la convierte en una fuga de información casi perfecta. Por esa razón se excluyó explícitamente de las variables predictoras, documentando la justificación semántica en vez de basar la decisión en si mejoraba o empeoraba una métrica.

El resto del pipeline de preparación (separación de columnas numéricas y categóricas, imputación y escalado/one-hot dentro de un `ColumnTransformer`) sigue el mismo patrón ya validado en el LAB01 con SVM sobre el dataset de referencia, reutilizando la misma disciplina de evitar fugas de datos manteniendo el preprocesamiento dentro del Pipeline. Los resultados finales de la comparación entre el clasificador base (`DummyClassifier`) y el modelo SVM quedan pendientes de completar una vez se reciba la aprobación formal del docente sobre la elección de este dataset, tal como exige el manual del laboratorio antes de continuar con el entrenamiento final.
