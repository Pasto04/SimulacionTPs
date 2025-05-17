import math
import random
from distributions.distribution import Distribution

class PoissonDistribution(Distribution):
    dist_name = "poisson"
    def __init__(self, lambda_: float):
        PoissonDistribution.params = {'lambda': lambda_}
        
    @classmethod
    def get_instance(cls, lambda_: float):
        if cls.instance is None:
            cls.instance = cls(lambda_)
        return cls.instance
    

    @classmethod
    def randomFromRejectionMethod(cls):
        lambda_ = cls.params['lambda']
        if lambda_ <= 0:
            cls.rejection_method_generated_numbers.append(0)
            return

        b = 0.931 + 2.53 * math.sqrt(lambda_)
        a = -0.059 + 0.02483 * b
        inv_alpha = 1.1239 + 1.1328 / (b - 3.4)
        vr = 0.9277 - 3.6224 / (b - 2)

        while True:
            u = random.random() - 0.5
            v = random.random()
            us = 0.5 - abs(u)
            k = int(math.floor((2 * a / us + b) * u + lambda_ + 0.43))
            if k < 0:
                continue

            if us >= 0.07 and v <= vr:
                cls.rejection_method_generated_numbers.append(k)
                break

            log_p = -lambda_ + k*math.log(lambda_) - math.lgamma(k+1)
            log_q = math.log(v * inv_alpha / (us*us))
            if log_q <= log_p:
                cls.rejection_method_generated_numbers.append(k)
                break
