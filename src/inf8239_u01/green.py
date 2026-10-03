import pandas as pd


def pareto_flags(df: pd.DataFrame, score: str, cost: str) -> pd.Series:
    """
    Marca que filas de `df` pertenecen a la frontera de Pareto al maximizar
    `score` y minimizar `cost`.

    Una fila A domina a una fila B si A es al menos tan buena como B en
    ambos objetivos y estrictamente mejor en al menos uno:
    A[score] >= B[score] and A[cost] <= B[cost], con desigualdad estricta
    en alguno de los dos. Una fila que ninguna otra domina queda marcada
    como perteneciente a la frontera (True).

    Parameters
    ----------
    df : pd.DataFrame
        Tabla con al menos las columnas `score` y `cost`.
    score : str
        Nombre de la columna a maximizar (p. ej. "f1_macro").
    cost : str
        Nombre de la columna a minimizar (p. ej. "fit_median_s").

    Returns
    -------
    pd.Series (bool), con el mismo indice que `df`.
    """
    if df.empty:
        return pd.Series([], dtype=bool, index=df.index)

    scores = df[score].to_numpy()
    costs = df[cost].to_numpy()
    n = len(df)
    flags = [True] * n

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            at_least_as_good = scores[j] >= scores[i] and costs[j] <= costs[i]
            strictly_better = scores[j] > scores[i] or costs[j] < costs[i]
            if at_least_as_good and strictly_better:
                flags[i] = False
                break

    return pd.Series(flags, index=df.index)
