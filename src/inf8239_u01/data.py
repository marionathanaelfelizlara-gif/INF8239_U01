from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _resolve(path_like) -> Path:
    """Convierte una ruta relativa en absoluta, anclada a la raiz del proyecto.
    Si ya es absoluta, se respeta tal cual."""
    p = Path(path_like)
    return p if p.is_absolute() else (PROJECT_ROOT / p)


def build_dataset_from_excel(xlsx_path: str, destination="data/raw/dataset.csv") -> Path:
    """Combina las 3 hojas del Excel de robos (MIP) en un solo dataset tabular.

    Fuente: https://datos.gob.do/dataset/estadisticas-de-robos-de-automotores-armas-de-fuego-y-denuncias-de-robos
    El archivo original viene en 3 hojas con esquemas distintos (ROBOS_AUTOMOTOR,
    ROBOS_ARMAS_FUEGO, ROBOS_GENERALES). Se unifican columnas y se agrega
    'categoria_robo' como variable de origen, que sirve como target de
    clasificacion (3 clases: Automotor, Armas de Fuego, General).
    """
    xlsx_path = _resolve(xlsx_path)
    if not xlsx_path.exists():
        raise FileNotFoundError(f"No se encontro el archivo fuente: {xlsx_path}")

    auto = pd.read_excel(xlsx_path, sheet_name="ROBOS_AUTOMOTOR").rename(columns={
        "AÑOS": "anio", "MESES": "mes", "PROVINCIA": "provincia",
        "CLASIFICACIÓN DEL VEHÍCULO": "tipo_detalle",
        "CANTIDAD DE DENUNCIAS POR ROBO DE VEHÍCULOS": "cantidad_denuncias",
    })
    auto["categoria_robo"] = "Automotor"

    armas = pd.read_excel(xlsx_path, sheet_name="ROBOS_ARMAS_FUEGO").rename(columns={
        "AÑOS": "anio", "MESES": "mes", "PROVINCIA": "provincia",
        "ROBO ARMAS DE FUEGO": "cantidad_denuncias",
    })
    armas["tipo_detalle"] = pd.NA
    armas["categoria_robo"] = "Armas de Fuego"

    gral = pd.read_excel(xlsx_path, sheet_name="ROBOS_GENERALES").rename(columns={
        "AÑOS": "anio", "MESES": "mes", "PROVINCIAS": "provincia",
        "TIPO DE ROBO": "tipo_detalle",
        "CANTIDAD DE DENUNCIAS POR ROBO DE GENERALES": "cantidad_denuncias",
    })
    gral["categoria_robo"] = "General"

    cols = ["anio", "mes", "provincia", "categoria_robo", "tipo_detalle", "cantidad_denuncias"]
    combined = pd.concat([auto[cols], armas[cols], gral[cols]], ignore_index=True)

    if combined.empty:
        raise ValueError("El dataset combinado esta vacio")

    path = _resolve(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(path, index=False)
    return path
