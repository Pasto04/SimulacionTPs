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

def main():
    generated_numbers = [ExponentialDistribution.randomFromRejectionMethod(5) for _ in range(15000)]
    #print(generated_numbers)
    print("Promedio: " , np.mean(generated_numbers))
    #print("Desviacion estandar: " , np.std(generated_numbers))


if __name__ == "__main__":
    main()

