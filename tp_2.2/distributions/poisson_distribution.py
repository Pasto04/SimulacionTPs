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

        b = 0.931 + 2.53 * math.sqrt(lambda_)
        a = -0.059 + 0.02483 * b
        inv_alpha = 1.1239 + 1.1328 / (b - 3.4)
        vr = 0.9277 - 3.6224 / (b - 2)

        while True:
            u = self.rng.random() - 0.5
            v = self.rng.random()
            us = 0.5 - abs(u)
            k = int(math.floor((2 * a / us + b) * u + lambda_ + 0.43))
            if k < 0:
                continue

            if us >= 0.07 and v <= vr:
                self.rejection_method_generated_numbers.append(k)
                break

            log_p = -lambda_ + k*math.log(lambda_) - math.lgamma(k+1)
            log_q = math.log(v * inv_alpha / (us*us))
            if log_q <= log_p:
                self.rejection_method_generated_numbers.append(k)
                break
