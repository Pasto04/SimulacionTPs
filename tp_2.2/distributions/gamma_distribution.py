import math
import random
from distributions.distribution import Distribution
class GammaDistribution(Distribution):
    dist_name = "gamma"
    def __init__(self, alpha: float, beta: float = 1):
        GammaDistribution.params = {"alpha": alpha, "beta": beta}
        
    @classmethod
    def get_instance(cls, alpha: float, beta: float = 1):
        if cls.instance is None:
            cls.instance = cls(alpha,beta)
        return cls.instance
    
    @classmethod
    def randomFromRejectionMethod(cls):
        alpha = cls.params['alpha']
        beta = cls.params['beta']
        if alpha < 1:
            while True:
                u = random.random()
                v = random.random()
                x = (-math.log(u)) ** (1 / alpha)
                y = math.exp(-x)
                if v <= y:
                    cls.rejection_method_generated_numbers.append(x / beta)
                    break
        else:
            d = alpha - 1/3
            c = 1 / math.sqrt(9 * d)

            while True:
                z = random.gauss(0, 1)
                u = random.random()
                v = (1 + c * z) ** 3

                if v > 0 and math.log(u) < (0.5 * z**2 + d - d * v + d * math.log(v)):
                    cls.rejection_method_generated_numbers.append(d * v / beta)
                    break
        