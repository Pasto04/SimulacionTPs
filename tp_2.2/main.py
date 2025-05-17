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
from tests import Tests

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
    
    for _ in range(15000):
        UniformDistribution.randomFromInverseTransform()
        UniformDistribution.randomFromRejectionMethod()
        ExponentialDistribution.randomFromInverseTransform()
        ExponentialDistribution.randomFromRejectionMethod()
        #GammaDistribution.randomFromRejectionMethod()
        #NormalDistribution.randomFromInverseTransform()
        #NormalDistribution.randomFromRejectionMethod()
        #PascalDistribution.randomFromRejectionMethod()
        #BinomialDistribution.randomFromRejectionMethod()
        #HypergeometricDistribution.randomFromRejectionMethod() 
        #PoissonDistribution.randomFromRejectionMethod()    
        EmpiricalDiscreteDistribution.randomFromRejectionMethod()
    distributions: list[Distribution] = [
        #normal_distribution,
        exponential_distribution,
        uniform_distribution,
        #binomial_distribution,
        #poisson_distribution,
        #emprical_discrete_distribution
    ]
    random_numbers = normal_distribution.getInverseTransformGeneratedNumbers()
    return distributions
    

def test_distributions(distributions: list[Distribution]):
      
    for dist in distributions:
        if (len(dist.getRejectionMethodGeneratedNumbers()) > 0):
            chi2_stat, p, passed = Tests.frequency_test(dist.getRejectionMethodGeneratedNumbers(), dist.getParams(), dist_name=dist.getDistName())
            print(f"Chi2 test for {dist.dist_name} distribution: {chi2_stat}, p-value: {p}, passed: {passed}")
        if (len(dist.getInverseTransformGeneratedNumbers()) > 0):
            chi2_stat, p, passed = Tests.frequency_test(dist.getInverseTransformGeneratedNumbers(), dist.getParams(), dist_name=dist.getDistName())
            print(f"Chi2 test for {dist.dist_name} distribution: {chi2_stat}, p-value: {p}, passed: {passed}")
        

    


def main():
    distributions = generate_distributions()
    test_distributions(distributions)




if __name__ == "__main__":
    main()

