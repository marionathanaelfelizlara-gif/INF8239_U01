# INF-8239 · Ciencia de Datos II — Unidad 01

Proyecto de laboratorios guiados de la Unidad 01: **LAB00** (configuración del entorno), **LAB01** (clasificación SVM sobre un dataset de referencia), **LAB02** (búsqueda, selección y auditoría de un dataset público) y **LAB03** (ensambles, reducción dimensional y Green AI).

## Instalación

```
python -m venv .venv
.venv\Scripts\activate
pip install -r Requirements.txt
```

Para ejecutar notebooks y pruebas, asegúrate de que el kernel/entorno seleccionado en VS Code sea el `.venv` del proyecto (no el Python global del sistema).

---

## LAB01 — Clasificación SVM (dataset de referencia)

**Pregunta de investigación:** ¿es posible clasificar correctamente un tumor como maligno o benigno a partir de sus características morfológicas?

- **Dataset:** Breast Cancer Wisconsin (`sklearn.datasets.load_breast_cancer`) — 569 muestras, 30 características numéricas por muestra de tejido mamario.
- **Target:** diagnóstico binario (0 = maligno, 212 casos; 1 = benigno, 357 casos).
- **División:** 455 train / 114 test, estratificada.
- **Métrica:** F1-macro.
- **Aviso:** ejercicio con fines exclusivamente académicos; no constituye una herramienta de diagnóstico médico real.

### Resultados

| Modelo | F1-macro |
|---|---|
| Baseline (`DummyClassifier`) | 0.387 |
| SVM (`StandardScaler` + `SVC` kernel rbf) en test | 0.9812 |

Métricas adicionales del modelo SVM sobre el conjunto de test: **accuracy 0.9825**, **ROC-AUC 0.995**.

**Búsqueda de hiperparámetros** (`GridSearchCV` + `StratifiedKFold` sobre C y gamma) — mejor combinación: `C=10, gamma=0.01`, F1-macro en validación cruzada = **0.9739**.

| C | gamma | F1-macro (CV) |
|---|---|---|
| 0.1 | scale | 0.938 |
| 0.1 | 0.01 | 0.942 |
| 0.1 | 0.1 | 0.934 |
| 1.0 | scale | 0.967 |
| 1.0 | 0.01 | 0.969 |
| 1.0 | 0.1 | 0.953 |
| 10.0 | scale | 0.967 |
| **10.0** | **0.01** | **0.974** |
| 10.0 | 0.1 | 0.938 |

(tabla completa en [`reports/svm_cv_results.csv`](reports/svm_cv_results.csv))

**Ejecución:** `notebooks/01_svm_guiada.ipynb` (Run All). El modelo final se guarda en `reports/svm_best.joblib`.

---

## LAB02 — Dataset público: Robos de Automotores, Armas de Fuego y Denuncias de Robo

**Dataset elegido:** Estadísticas de Robos de Automotores, Armas de Fuego y Denuncias de Robos (Ministerio de Interior y Policía, vía [datos.gob.do](https://datos.gob.do/dataset/estadisticas-de-robos-de-automotores-armas-de-fuego-y-denuncias-de-robos), licencia ODbL). Ver procedencia y comparación con el candidato descartado (Turismo Cultural / MITUR) en [`docs/ficha_dataset.md`](docs/ficha_dataset.md), y el diccionario de columnas en [`docs/diccionario_datos.md`](docs/diccionario_datos.md).

### Descarga / construcción del dataset

El archivo fuente (`data/raw/robos-automotor-armas-de-fuego-y-denuncias-de-robo-2018-2025.xlsx`) está versionado en este repositorio (ver `.gitignore`), porque el flujo usa el Excel oficial con sus 3 hojas en vez de una URL de descarga directa. Para regenerar `data/raw/dataset.csv`:

```python
from inf8239_u01.data import build_dataset_from_excel
build_dataset_from_excel("data/raw/robos-automotor-armas-de-fuego-y-denuncias-de-robo-2018-2025.xlsx")
```

Ya automatizado en la primera celda de código de `notebooks/02_dataset_publico.ipynb`.

### Target y métrica

- **Target:** `categoria_robo` (3 clases: Automotor, Armas de Fuego, General). 6,516 filas, sin duplicados.
- **Métrica:** F1-macro (da igual peso a las 3 clases; relevante porque Armas de Fuego es la clase minoritaria y la de error más costoso).
- **Columna excluida de X:** `tipo_detalle`, por fuga de información (sus valores son proxy casi perfecto del target — ver justificación completa en `docs/ficha_dataset.md` y en el paso 7 del notebook).

### Resultados

| Modelo | F1-macro (test) |
|---|---|
| Baseline (`DummyClassifier`, most_frequent) | 0.208 |
| SVM (`ColumnTransformer` + `SVC`) | 0.552 |

Detalle por clase del modelo SVM:

| Clase | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Armas de Fuego | 0.42 | 0.05 | 0.08 | 212 |
| Automotor | 0.68 | 0.71 | 0.69 | 499 |
| General | 0.78 | 1.00 | 0.88 | 593 |

El SVM mejora ampliamente al baseline en conjunto, pero **falla específicamente en la clase que definimos como de error más costoso** (Armas de Fuego, recall = 0.05): el modelo casi nunca la predice correctamente, probablemente porque las únicas variables disponibles (año, mes, provincia, cantidad de denuncias) no bastan para distinguirla de las otras categorías una vez retirada `tipo_detalle`.

**Ejecución:**

```
notebooks/02_dataset_publico.ipynb   (Run All)
```

```
set PYTHONPATH=src
python -m pytest -q
```

> **Nota:** el paso 9 (entrenamiento SVM vs. baseline) es el entrenamiento final del modelo y, según el manual del laboratorio, requiere aprobación previa del docente sobre el dataset elegido antes de tomarse como resultado definitivo de entrega.

---

## LAB03 — Ensambles, reducción dimensional y Green AI

Reutiliza, sin cambios, el dataset, target, columna excluida (`tipo_detalle`) y partición (80/20 estratificada, `random_state=42`) del LAB02. **Métrica principal:** F1-macro. **Clase prioritaria** (error más costoso, heredada del LAB02): Armas de Fuego.

### Catálogo de modelos comparados

Seis configuraciones sobre el mismo `ColumnTransformer`, más una variante con reducción de dimensionalidad (PCA), medidas con mediana de 3 repeticiones de entrenamiento, tiempo de predicción y tamaño en disco:

| Modelo | F1-macro (test) | Entrenamiento (mediana, s) | Predicción (ms) | Tamaño en disco (KB) | ¿Frontera de Pareto? |
|---|---|---|---|---|---|
| HistGradientBoosting | 0.682 | 1.76 | 34.7 | 1,070.6 | Sí |
| Regresión logística | 0.676 | 0.06 | 5.4 | 5.9 | Sí |
| Random Forest (300 árboles) | 0.632 | 3.40 | 142.1 | 81,528.9 | No |
| Random Forest (100 árboles) | 0.629 | 0.82 | 76.1 | 27,085.6 | No |
| SVM (C=10) | 0.618 | 0.71 | 340.1 | 1,254.5 | No |
| SVM (C=1) | 0.552 | 0.63 | 300.9 | 1,277.1 | No |
| SVM (C=1) + PCA | 0.552 | 1.28 | 439.6 | 1,278.0 | No |

(tabla completa en [`reports/green_ai_results.csv`](reports/green_ai_results.csv); modelos serializados en `reports/models/*.joblib`)

### PCA y t-SNE

El bloque numérico de este dataset solo tiene 2 columnas (`anio`, `cantidad_denuncias`), así que `PCA(n_components=.95)` retiene ambas componentes: no hay reducción real de dimensionalidad que demostrar, solo el costo de calcularla — por eso SVM+PCA entrena el doble de lento que el SVM equivalente sin PCA (1.28s vs. 0.63s) y llega exactamente al mismo F1-macro (0.552). Es la lección esperada: PCA no ayuda cuando el espacio numérico de partida ya es mínimo.

Los dos mapas t-SNE (semillas 42 y 7, [`reports/tsne_two_seeds.png`](reports/tsne_two_seeds.png)) muestran formas de grupo casi idénticas entre semillas — señal de que la proyección es estable, no un artefacto de la optimización. Aun así, construida solo con las 2 variables numéricas, las clases no se separan con claridad: "General" y "Automotor" forman cadenas reconocibles, mientras que "Armas de Fuego" aparece dispersa dentro de ambas regiones sin un clúster propio, consistente con el bajo recall que ya tenía esa clase en el LAB02.

### Frontera de Pareto y decisión

([`reports/pareto.png`](reports/pareto.png))

Dos modelos quedan en la frontera de Pareto (ninguno los domina a la vez en F1 y en tiempo): **HistGradientBoosting** (F1=0.682, el más preciso) y **regresión logística** (F1=0.676, el más barato). Los otros cinco (ambos Random Forest, ambos SVM con y sin PCA) quedan dominados: tienen F1 igual o menor que uno de los dos anteriores y además tardan más en entrenarse.

**Decisión cuantificada:** la regresión logística sacrifica solo **0.006 puntos de F1-macro** (0.676 vs. 0.682, menos del 1% de diferencia relativa) a cambio de **~96.6% menos tiempo de entrenamiento** (0.06s vs. 1.76s), **~99.4% menos tamaño en disco** (5.9 KB vs. 1,070.6 KB) y **~84.6% menos tiempo de predicción** (5.4ms vs. 34.7ms). Para un escenario que prioriza bajo costo computacional (Green AI), la regresión logística es la elección razonable; solo si la prioridad fuera maximizar F1-macro sin importar el costo tendría sentido HistGradientBoosting. Los Random Forest son la evidencia más clara de costo sin retorno en este catálogo: el de 300 árboles pesa 81.5 MB en disco (~14,000 veces más que la regresión logística) sin superar el F1 de ninguno de los dos modelos de la frontera.

**Limitación:** esta comparación usa F1-macro (la métrica principal declarada para el LAB03), no el detalle por clase; antes de llevar cualquiera de estos modelos a producción habría que revisar también el recall específico sobre Armas de Fuego, que no se midió en esta tabla.

### Entorno de medición

Los tiempos se midieron en la máquina del estudiante, en un único momento, bajo la carga que tuviera el sistema en ese instante — **no es una medición de energía ni de huella de carbono real**; aquí "Green AI" se limita a comparar costo computacional relativo entre modelos. Detalle de plataforma impreso en el paso 9 de `notebooks/03_ensambles_green_ai.ipynb`.

**Ejecución:**

```
notebooks/03_ensambles_green_ai.ipynb   (Run All)
```

```
set PYTHONPATH=src
python -m pytest tests/test_green.py -v
```

---

## Estructura del repositorio

```
data/raw/       Dataset fuente (.xlsx) y generado (dataset.csv, no versionado)
docs/           Ficha del dataset, diccionario de datos y guía de ejecución del LAB03
notebooks/      Notebooks guiados de cada laboratorio (00, 01, 02, 03)
reports/        Resultados guardados (cv_results, green_ai_results.csv, figuras, modelos .joblib)
src/            Código fuente reutilizable (paquete inf8239_u01, incluye green.py)
tests/          Pruebas automatizadas (pytest)
```

---

## Conclusión

Este trabajo recorrió dos escenarios deliberadamente distintos. El LAB01 partió de un dataset de referencia limpio y ya empaquetado (Breast Cancer Wisconsin), lo que permitió concentrarse en la disciplina metodológica en sí: separar entrenamiento y prueba de forma estratificada, establecer un baseline honesto con `DummyClassifier` antes de entrenar cualquier modelo, mantener todo el preprocesamiento (`StandardScaler`) dentro de un `Pipeline` para evitar fugas de información entre el ajuste y la evaluación, y usar `GridSearchCV` con validación cruzada estratificada para afinar hiperparámetros de forma reproducible. El resultado, un F1-macro de 0.98 y ROC-AUC de 0.995, confirma que sobre un dataset ya curado el reto principal es aplicar bien el método, no lidiar con los datos.

El LAB02 invirtió esa relación. Aquí el reto no fue el modelo sino el dataset: un archivo público real, dividido en 3 hojas de Excel con esquemas de columnas distintos entre sí y sin una URL de descarga reproducible estándar, lo que obligó a construir una función propia (`build_dataset_from_excel`) para unificarlas en un solo dataset tabular versionado junto con su fuente original. La auditoría posterior reveló que el 16.3% de valores ausentes en `tipo_detalle` no era un problema de calidad de datos, sino la pista de algo más serio: esa columna es un proxy casi perfecto del target, y se excluyó del modelo por esa razón semántica, no porque afectara la métrica. Aplicando la misma disciplina metodológica del LAB01 (`ColumnTransformer` para separar variables numéricas y categóricas, partición estratificada, comparación contra un baseline), el SVM resultante alcanzó un F1-macro de 0.552 frente a 0.208 del baseline — una mejora clara en conjunto, pero con una falla puntual reveladora: la clase Armas de Fuego, que habíamos identificado de antemano como la de error más costoso, obtuvo un recall de apenas 0.05. El modelo prácticamente no logra reconocerla con las variables disponibles una vez retirada la columna que hacía fuga de información.

La lección conjunta de ambos laboratorios es que la misma metodología (evitar fugas, medir contra un baseline, validar con validación cruzada) produce resultados muy distintos según la naturaleza del dataset: en datos curados el techo de desempeño es alto y el trabajo es sobre todo de ejecución; en datos públicos reales, gran parte del valor está en la auditoría misma — detectar qué columnas no se pueden usar y por qué — y los resultados finales deben leerse junto con sus limitaciones, no solo como una cifra de métrica.

El LAB03 añadió una tercera dimensión a esa disciplina metodológica: el costo computacional. Comparar seis configuraciones de modelo bajo el mismo protocolo congelado del LAB02, midiendo tiempo de entrenamiento (mediana de 3 repeticiones), tiempo de predicción y tamaño en disco junto al F1-macro, dejó una frontera de Pareto de solo dos modelos no dominados: HistGradientBoosting, el más preciso, y una regresión logística casi igual de buena (diferencia de apenas 0.006 en F1-macro) pero cientos de veces más barata de entrenar y de almacenar. La reducción dimensional (PCA) no aportó nada aquí porque el bloque numérico de este dataset ya era mínimo (solo 2 columnas), y los dos mapas t-SNE confirmaron con otra técnica lo que el LAB02 ya había mostrado: la clase Armas de Fuego no se distingue bien con las variables numéricas disponibles. La lección final de los tres laboratorios es que ni el modelo más sofisticado ni el más grande es automáticamente el mejor: la pregunta correcta no es solo "¿cuál tiene el F1 más alto?", sino "¿cuánto cuesta esa diferencia de F1, y vale la pena pagarlo?" — y esa pregunta solo se puede responder si se mide el costo, no solo la métrica.
