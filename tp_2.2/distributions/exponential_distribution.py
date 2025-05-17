import math
import random
from distributions.distribution import Distribution
class ExponentialDistribution(Distribution):
    dist_name = "exponential"

    def __init__(self, lambda_: float):
        ExponentialDistribution.params = {"lambda": lambda_}
        
    @classmethod
    def get_instance(cls, lambda_: float):
        if cls.instance is None:
            cls.instance = cls(lambda_)
        return cls.instance
    
    @classmethod
    def randomFromInverseTransform(cls):
        lambda_ = cls.params['lambda']
        r = random.random()
        x = - (1 / lambda_) * math.log(r)
        cls.inverse_transform_generated_numbers.append(x)

    @classmethod
    def randomFromRejectionMethod(cls):
        lambda_ = cls.params['lambda']
        x_max = -math.log(0.0001) / lambda_ 
        y_max = lambda_       

        while True:
            x = random.uniform(0, x_max)
            y = random.uniform(0, y_max)
            fx = lambda_ * math.exp(-lambda_ * x)
            if y <= fx:
                cls.rejection_method_generated_numbers.append(x)
                break

