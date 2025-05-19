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
from distributions.distribution import Distribution
from tabulate import tabulate
from tests import Tests

NUM_RANDOM_VALUES = 1000
NUM_INTERVALS = 10

def generate_distributions():

    normal_distribution = NormalDistribution.get_instance(mu=25, sigma=4)
    exponential_distribution = ExponentialDistribution.get_instance(lambda_=0.2)
    uniform_distribution = UniformDistribution.get_instance(a=0, b=50)
    binomial_distribution = BinomialDistribution.get_instance(n=10, p=0.5)
    poisson_distribution = PoissonDistribution.get_instance(lambda_=5)
    hypergeometric_distribution = HypergeometricDistribution.get_instance(N=50, K=10, n=5)
    pascal_distribution = PascalDistribution.get_instance(r=5, p=0.5)
    gamma_distribution = GammaDistribution.get_instance(alpha=2, beta=2)
    emprical_discrete_distribution = EmpiricalDiscreteDistribution.get_instance(values=[1, 2, 3, 4, 5], probs=[0.1, 0.2, 0.3, 0.2, 0.2])

    for _ in range(NUM_RANDOM_VALUES):
        uniform_distribution.randomFromInverseTransform()
        uniform_distribution.randomFromRejectionMethod()
        exponential_distribution.randomFromInverseTransform()
        exponential_distribution.randomFromRejectionMethod()
        gamma_distribution.randomFromRejectionMethod()
        normal_distribution.randomFromInverseTransform()
        normal_distribution.randomFromRejectionMethod()
        pascal_distribution.randomFromRejectionMethod()
        binomial_distribution.randomFromRejectionMethod()
        hypergeometric_distribution.randomFromRejectionMethod() 
        poisson_distribution.randomFromRejectionMethod()    
        emprical_discrete_distribution.randomFromRejectionMethod() 

    distributions: list[Distribution] = [
        normal_distribution,
        exponential_distribution,
        uniform_distribution,
        binomial_distribution,
        poisson_distribution,
        emprical_discrete_distribution
    ]

    return distributions
    

def test_distributions(distributions: list[Distribution]):
    general_results = {}

    try:
        for dist in distributions:
            rejection_method_numbers = dist.getRejectionMethodGeneratedNumbers()
            if (len(rejection_method_numbers) > 0):
                results = Tests.all_tests(rejection_method_numbers, dist.getParams(), dist_name=dist.getDistName(), num_intervals=NUM_INTERVALS)
                show_distribution_results(results, rejection_method_numbers, f"{dist.getDistName()} - Método Rechazo", general_results)
            
            inverse_transform_numbers = dist.getInverseTransformGeneratedNumbers()
            if (len(inverse_transform_numbers) > 0):
                results = Tests.all_tests(inverse_transform_numbers, dist.getParams(), dist_name=dist.getDistName(), num_intervals=NUM_INTERVALS)
                show_distribution_results(results, inverse_transform_numbers, f"{dist.getDistName()} - Transformada Inversa", general_results)
            
        print("\nResumen de tests:")
        headers = ["Distribución", "Chi²", "KS", "AD", "Media", "Desv. Std"]
        table_data = []
        for name, res in general_results.items():
            row = [
                name.replace("_", " ").title(),
                res["Chi2"],
                res["KS"],
                res["AD"],
                #res["Media"],
                #res["Desv. Std"]
            ]
            table_data.append(row)
        
        print("✓: Pasó el test - X: No pasó el test")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    except Exception as e:
        print(f"⚠️ Error en la prueba de {dist.getDistName()}: {e}")


def show_distribution_results(results, numbers, dist_name, general_results):
    print(f"\n--- Probando distribución: {dist_name.upper()} ---")
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

    print("Promedio:", np.mean(numbers))
    print("Desviación estándar:", np.std(numbers))

    general_results[dist_name] = {
        "Chi2": "✓" if isinstance(results['Chi2'], tuple) and results['Chi2'][2] else "X",
        "KS": "✓" if isinstance(results['KS'], tuple) and results['KS'][2] else "X",
        "AD": "✓" if isinstance(results['AD'], tuple) and results['AD'][2] else "X",
        #"Media": f"{np.mean(dist.getDistName()):.2f}",  #acá está el error
        #"Desv. Std": f"{np.std(dist.getDistName()):.2f}"
    }       


def main():
    distributions = generate_distributions()
    test_distributions(distributions)


if __name__ == "__main__":
    main()
