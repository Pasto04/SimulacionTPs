import math
from scipy.stats import poisson
import numpy as np
from distributions.distribution import Distribution

class PoissonDistribution(Distribution):
    dist_name = "poisson"
    dist_type = "discrete"
    
    def __init__(self, lambda_: float, seed:int=12345):
        super().__init__(seed)
        self.params = {'lambda': lambda_}
        
    @classmethod
    def get_instance(cls, lambda_: float):
        if cls.instance is None:
            cls.instance = cls(lambda_)
        return cls.instance

    def getParams(self):
        return self.params

    def get_expected_pmf(self):
        lambda_ = self.params["lambda"]
        
        x_max = int(3 * lambda_)
        x = np.arange(0, x_max + 1)
        
        pdf = poisson.pmf(x, lambda_)

        return x, pdf


    def randomFromRejectionMethod(self):
        lambda_ = self.params['lambda']
        if lambda_ <= 0:
            self.rejection_method_generated_numbers.append(0)
            return

        c = 0.767 - 3.36 / lambda_
        beta = math.pi / math.sqrt(3.0 * lambda_)
        alpha = beta * lambda_
        k = math.log(c) - lambda_ - math.log(beta)

        while True:
            u = self.rng.random()
            x = (alpha - math.log((1.0 - u) / u)) / beta
            n = int(math.floor(x + 0.5))
            if n < 0:
                continue
            v = self.rng.random()
            y = alpha - beta * x
            lhs = y + math.log(v / ((1.0 + math.exp(y))**2))
            rhs = k + n * math.log(lambda_) - math.lgamma(n + 1)
            if lhs <= rhs:
                self.rejection_method_generated_numbers.append(n)
                break
