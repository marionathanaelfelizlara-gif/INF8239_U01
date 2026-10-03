import pandas as pd

from inf8239_u01.green import pareto_flags


def test_dominated_model_is_excluded():
    df = pd.DataFrame({
        "model": ["rapido_impreciso", "lento_preciso", "dominado"],
        "f1_macro": [0.80, 0.85, 0.60],
        "fit_median_s": [1.0, 1.2, 1.5],
    }).set_index("model")

    flags = pareto_flags(df, score="f1_macro", cost="fit_median_s")

    # "dominado" tiene peor f1 (0.60) Y peor tiempo (1.5s) que
    # "rapido_impreciso" (0.80, 1.0s): queda dominado y fuera de la frontera.
    assert flags["dominado"] == False
    # Los otros dos representan un trade-off real (uno es mas rapido, el
    # otro mas preciso), asi que ambos quedan en la frontera.
    assert flags["rapido_impreciso"] == True
    assert flags["lento_preciso"] == True


def test_tied_models_both_stay_on_frontier():
    df = pd.DataFrame({
        "model": ["gemelo_1", "gemelo_2"],
        "f1_macro": [0.75, 0.75],
        "fit_median_s": [2.0, 2.0],
    }).set_index("model")

    flags = pareto_flags(df, score="f1_macro", cost="fit_median_s")

    # Ningun modelo domina estrictamente al otro (mismo f1, mismo tiempo),
    # asi que ninguno queda excluido de la frontera.
    assert flags["gemelo_1"] == True
    assert flags["gemelo_2"] == True
