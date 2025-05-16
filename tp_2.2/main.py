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
from tests import Tests

dist = {
        "params": [],
        "generated_numbers": [],
    }

distributions = {
    "uniform": {
        "params": {"a": 10, "b": 20}, 
        "generated_numbers": [],
    },
    "exponential": {
        "params": {"lambda": 0.5},    
        "generated_numbers": [],
    },
    "normal": {
        "params": {"mu": 25, "sigma": 4},  
        "generated_numbers": [],
    },
    "binomial": {
        "params": {"n": 20, "p": 0.3},  
        "generated_numbers": [],
    },
    "poisson": {
        "params": {"mu": 6},           
        "generated_numbers": [],
    },
    "emp_discrete": {
        "params": {
            "values": [1, 2, 3, 4, 5],
            "probs": [0.1, 0.2, 0.4, 0.2, 0.1],  
        },
        "generated_numbers": [],
    },
}



def main():
    
    distributions['normal']['generated_numbers'] = [NormalDistribution.randomFromRejectionMethod(distributions['normal']['params']['mu'],distributions['normal']['params']['sigma']) for _ in range(15000)]
    chi2_stat, p, passed = Tests.frequency_test(distributions['normal']['generated_numbers'], {'mu':25, 'sigma':4}, dist_name = 'normal')
    
    print(distributions['normal']['generated_numbers'])

    print("Chi2: ", chi2_stat)
    print("p-value: ", p)
    print("Prueba de Chi2: ", "Aprobada" if passed else "Rechazada")  
    print("Promedio: " , np.mean(distributions['normal']['generated_numbers']))
    print("Desviacion estandar: " , np.std(distributions['normal']['generated_numbers']))


if __name__ == "__main__":
    main()

