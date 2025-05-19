"""
Pseudo-random number generators for different probability distributions
Dev Team:
    - Cosentino, Lucio Nahuel
    - Danteo, Elías Tomás
    - De Bernardo, Aarón
    - Fernandez Da Silva, Joaquín C.
    - Malizani, Juan Pablo
    - Pastorino, Juan José
"""

import numpy as np
from distributions.uniform_distribution import UniformDistribution
from distributions.exponential_distribution import ExponentialDistribution
from distributions.normal_distribution import NormalDistribution
from distributions.gamma_distribution import GammaDistribution
from distributions.binomial_distribution import BinomialDistribution
from distributions.poisson_distribution import PoissonDistribution
from distributions.hypergeometric_distribution import HypergeometricDistribution
from distributions.empirical_discrete_distribution import EmpiricalDiscreteDistribution
from distributions.pascal_distribution import PascalDistribution
from tabulate import tabulate

from tests import Tests

NUM_SAMPLES = 15000
NUM_INTERVALS = 10

test_results = {}

distributions = {
    "uniform": {
        "params": {"a": 10, "b": 20},
        "generator": lambda p: UniformDistribution.randomFromInverseTransform(p["a"], p["b"]),
    },
    "exponential": {
        "params": {"lambda": 0.5},
        "generator": lambda p: ExponentialDistribution.randomFromInverseTransform(p["lambda"]),
    },
    "normal": {
        "params": {"mu": 25, "sigma": 4},
        "generator": lambda p: NormalDistribution.randomFromRejectionMethod(p["mu"], p["sigma"]),
    },

    "binomial": {
        "params": {"n": 20, "p": 0.3},
        "generator": lambda p: BinomialDistribution.random_from_rejection_method(p["n"], p["p"]),
    },
    "poisson": {
        "params": {"mu": 6},
        "generator": lambda p: PoissonDistribution.randomFromRejectionMethod(p["mu"]),
    },
    "emp_discrete": {
        "params": {
            "values": [1, 2, 3, 4, 5],
            "probs": [0.1, 0.2, 0.4, 0.2, 0.1],
        },
        "generator": lambda p: EmpiricalDiscreteDistribution.random_from_rejection_method(p["values"], p["probs"]),
    },
    "pascal": {
        "params": {"r": 5, "p": 0.4},
        "generator": lambda p: PascalDistribution.randomFromRejectionMethod(p["r"], p["p"]),
    },

        "gamma": {
        "params": {"alpha": 2, "beta": 2},
        "generator": lambda p: GammaDistribution.randomFromRejectionMethod(p["alpha"], p["beta"]),
    },
    
    # "hypergeometric": {} 
    
}


def main():
    for name, info in distributions.items():
        params = info["params"]
        generator = info["generator"]

        print(f"\n--- Probando distribución: {name.upper()} ---")
        samples = [generator(params) for _ in range(NUM_SAMPLES)]
        try:
            results = Tests.all_tests(samples, params, dist_name=name, num_intervals=NUM_INTERVALS)

            if isinstance(results['Chi2'], tuple):
                chi2_stat, p_value, passed = results['Chi2']
                print(f"Chi2: {chi2_stat:.3f}")
                print(f"p-value: {p_value:.4f}")
                print("Resultado Chi2:", "✔️ Aprobada" if passed else "❌ Rechazada")
            else:
                print("Chi2:", results['Chi2'])

            if isinstance(results['KS'], tuple):
                ks_stat, ks_p, ks_passed = results['KS']
                print(f"KS: {ks_stat:.3f}")
                print(f"p-value KS: {ks_p:.4f}")
                print("Resultado KS:", "✔️ Aprobada" if ks_passed else "❌ Rechazada")
            else:
                print("KS:", results['KS'])

            if isinstance(results['AD'], tuple):
                ad_stat, ad_crit, ad_passed = results['AD']
                print(f"AD statistic: {ad_stat:.3f}")
                print(f"AD critical value (5%): {ad_crit:.3f}")
                print("Resultado AD:", "✔️ Aprobada" if ad_passed else "❌ Rechazada")
            else:
                print("AD:", results['AD'])

            print("Promedio:", np.mean(samples))
            print("Desviación estándar:", np.std(samples))

            test_results[name] = {
                "Chi2": "✓" if isinstance(results['Chi2'], tuple) and results['Chi2'][2] else "X",
                "KS": "✓" if isinstance(results['KS'], tuple) and results['KS'][2] else "X",
                "AD": "✓" if isinstance(results['AD'], tuple) and results['AD'][2] else "X",
                "Media": f"{np.mean(samples):.2f}",
                "Desv. Std": f"{np.std(samples):.2f}"
            }       

        except Exception as e:
            print(f"⚠️ Error en la prueba de {name}: {e}")

        print("\nResumen de tests:")
        headers = ["Distribución", "Chi²", "KS", "AD", "Media", "Desv. Std"]
        table_data = []

    for name, res in test_results.items():
        row = [
            name.replace("_", " ").title(),
            res["Chi2"],
            res["KS"],
            res["AD"],
            res["Media"],
            res["Desv. Std"]
        ]
        table_data.append(row)

    print("✓: Pasó el test - X: No pasó el test")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
