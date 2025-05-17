import math
import random
from distributions.distribution import Distribution
class NormalDistribution(Distribution):
    dist_name = "normal"
    def __init__(self, mu, sigma ):
        NormalDistribution.params = {"mu": mu, "sigma": sigma}
        
    @classmethod
    def get_instance(cls, mu = 0, sigma = 1):
        if cls.instance is None:
            cls.instance = cls(mu, sigma)
        return cls.instance

    @classmethod
    def randomFromInverseTransform(cls): # en realidad no es por el método de la transformada inversa
        mu = cls.params['mu']
        sigma = cls.params['sigma']
        total = 0
        for _ in range(12):
            r = random.random()
            total += r
        z = total - 6

        cls.inverse_transform_generated_numbers.append(mu + sigma * z)


    @classmethod
    def randomFromRejectionMethod(cls):
        mu = cls.params['mu']
        sigma = cls.params['sigma']
        while True:
            u1 = random.random()
            u2 = random.random()
            y1 = - math.log(u1)
            y2 = - math.log(u2)
      
            aux = (y1 - 1)**2 / 2
            if (y2 >= aux):
                abs_z = y1
                z = abs_z if random.random() >= 0.5 else -abs_z
                x = sigma * z + mu
                cls.rejection_method_generated_numbers.append(x)
                break

