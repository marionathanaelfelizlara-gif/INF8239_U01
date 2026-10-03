# Guía de ejecución — LAB03 (Ensambles, reducción dimensional y Green AI)

Esta guía es el paso a paso para correr `notebooks/03_ensambles_green_ai.ipynb`


## 0. Antes de abrir el notebook

1. Confirma que `notebooks/02_dataset_publico.ipynb` ya se ejecutó al menos
   una vez (necesitas que exista `data/raw/dataset.csv`). Si no lo tienes,
   corre primero ese notebook.
2. Abre `notebooks/03_ensambles_green_ai.ipynb` en VS Code.
3. Arriba a la derecha, en el selector de kernel, confirma que dice el
   entorno del proyecto (`.venv`), **no** el Python global. Si no estás
   seguro, selecciona el kernel y elige `.venv` manualmente.
4. Con el kernel correcto seleccionado, usa **Restart** (icono circular) y
   espera a que el número de ejecución se reinicie, y luego **Run All**.
   No ejecutes celda por celda salteando el orden: varias celdas reutilizan
   variables (`X`, `preprocess`, `results`, `REPORTS_DIR`, etc.) definidas en
   celdas anteriores.

## 1. Paso 1 — Congelar el protocolo

Qué hace: vuelve a leer `data/raw/dataset.csv`, recrea `X`, `y`,
`preprocess` y la partición `Xtr/Xte/ytr/yte` **exactamente** como quedaron
en el LAB02 (mismo `random_state=42`, mismo `test_size=0.20`, mismo
`stratify=y`).

Qué deberías ver impreso:
```
Filas train/test: 5212 1304
Metrica principal: f1_macro
Clase prioritaria: Armas de Fuego
```

Si ves un error de archivo no encontrado (`FileNotFoundError`), es porque
`data/raw/dataset.csv` no existe todavía — vuelve al punto 0.

## 2. Paso 2 — Catálogo de modelos

Qué hace: define 6 modelos (`logistic`, `svm_c1`, `svm_c10`, `rf_100`,
`rf_300`, `boost`), todos con el mismo preprocesamiento.

Qué deberías ver: la lista de las 6 llaves del diccionario `models`. No
hay entrenamiento todavía en este paso (es solo la definición).

## 3. Paso 3 — Medir tres veces (tiempo y tamaño)

Qué hace: entrena cada uno de los 6 modelos 3 veces (para sacar una
mediana de tiempo de entrenamiento), mide el tiempo de predicción y
guarda cada modelo entrenado en `reports/models/<nombre>.joblib`.

**Esta celda tarda más que las anteriores** (entrena 18 veces en total: 6
modelos × 3 repeticiones). Es normal que tome uno o varios minutos según
tu máquina — no la interrumpas.

Qué deberías ver: una línea impresa por modelo con su F1, tiempo de
entrenamiento, tiempo de predicción y tamaño en KB, y luego una tabla
(`results`) ordenada de mayor a menor F1-macro. También se crea
`reports/green_ai_results.csv`.

Guarda mentalmente (o anota) cuál modelo quedó con el F1-macro más alto —
lo vas a necesitar para el Paso 7.

## 4. Paso 4 — Comparar con y sin PCA

Qué hace: entrena una variante del SVM (`svm_c1`) aplicando PCA solo a las
columnas numéricas (`anio`, `cantidad_denuncias`).

Qué deberías ver: cuántos componentes retuvo el PCA (probablemente 2 de
2 — con solo dos columnas numéricas no hay mucho que reducir, esto es
esperado y está documentado en el notebook, no es un error) y el F1-macro
resultante para comparar contra `svm_c1` de la tabla del Paso 3.

## 5. Paso 5 — Dos mapas t-SNE

Qué hace: dibuja dos proyecciones t-SNE (semillas 42 y 7) usando solo las
columnas numéricas, coloreadas por clase.

Qué deberías ver: una figura con dos paneles lado a lado, guardada en
`reports/tsne_two_seeds.png`. Compara si la forma de los grupos se parece
entre ambos paneles (estabilidad) o cambia mucho (poca confiabilidad de
la proyección) — el notebook ya deja una nota al respecto.

## 6. Paso 6 — Frontera de Pareto

Qué hace: importa `pareto_flags` desde `inf8239_u01/green.py`, agrega la
fila de `svm_c1_pca` a la tabla de resultados, y marca con `True/False`
cuáles modelos están en la frontera (ninguno los domina en F1 *y* tiempo
a la vez).

Qué deberías ver: la tabla `results_full` con la columna `es_pareto`, y
`reports/green_ai_results.csv` actualizado con esa columna.

Si esta celda falla con `ModuleNotFoundError: No module named
'inf8239_u01.green'`, revisa que `src/inf8239_u01/green.py` exista (ya
debería estar en tu repo) y que la celda del Paso 1 (la que ajusta
`sys.path`) se haya ejecutado antes.

## 7. Paso 7 — Gráfico y decisión razonada

Primera celda de código: dibuja `reports/pareto.png` (tiempo de
entrenamiento vs. F1-macro, resaltando los modelos en la frontera).

Segunda parte (celda de texto/markdown): es una **plantilla para
completar a mano** con tus resultados reales — no la dejé prellenada
porque los números van a variar según tu máquina. Ahí tienes que:

1. Mirar la tabla `results_full` y el gráfico `reports/pareto.png`.
2. Completar cada `___` de la plantilla (modelo con mayor F1, alternativa
   elegida, diferencia de F1, % de tiempo ahorrado, diferencia de tamaño).
3. Escribir el párrafo final de 300-500 palabras integrando esos puntos.

Cuando tengas esos números reales, si quieres que te ayude a redactar el
párrafo final o a revisar que cumpla el conteo de palabras, compárteme
la tabla y lo armamos juntos.

## 8. Paso 8 — Probar la frontera de Pareto

Esto **no se corre dentro del notebook**. Abre una terminal en la raíz del
proyecto (`C:\INF8239_U01`) con el entorno `.venv` activado y corre:

```bash
pytest tests/test_green.py -v
```

Deberías ver 2 pruebas en verde (`PASSED`):
- `test_dominated_model_is_excluded`
- `test_tied_models_both_stay_on_frontier`

## 9. Paso 9 — Registrar el entorno

Qué hace: imprime tu plataforma, versión de Python, procesador y versión
de scikit-learn, con una nota aclarando que los tiempos medidos no
equivalen a una medición real de energía/CO2.

Copia esa salida — la necesitas para completar el campo "Contexto de
hardware" de la plantilla del Paso 7.

## 10. Después de ejecutar todo

1. Guarda el notebook (Ctrl+S) con todas las salidas visibles.
2. Confirma que se generaron: `reports/green_ai_results.csv`,
   `reports/models/*.joblib`, `reports/tsne_two_seeds.png`,
   `reports/pareto.png`.
3. Corre `pytest tests/test_green.py -v` (Paso 8) y confirma que pasan.
4. Sube los cambios:
   ```bash
   git add notebooks/03_ensambles_green_ai.ipynb src/inf8239_u01/green.py tests/test_green.py reports/ docs/guia_ejecucion_lab03.md
   git commit -m "LAB03: catalogo de modelos, PCA, t-SNE, frontera de Pareto y Green AI"
   git push
   ```
