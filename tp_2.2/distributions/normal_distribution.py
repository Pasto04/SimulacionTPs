import math
from distributions.distribution import Distribution
class NormalDistribution(Distribution):
    dist_name = "normal"

    def __init__(self, mu, sigma, seed:int =12345): 
        super().__init__(seed)
        self.params = {"mu": mu, "sigma": sigma}


    def getParams(self):
        return self.params


    @classmethod
    def get_instance(cls, mu = 0, sigma = 1):
        if cls.instance is None:
            cls.instance = cls(mu, sigma)
        return cls.instance

    
    def randomFromInverseTransform(self): # en realidad no es por el método de la transformada inversa
        mu = self.params['mu']
        sigma = self.params['sigma']
        total = 0
        for _ in range(12):
            r = self.rng.random()
            total += r
        z = total - 6

        self.inverse_transform_generated_numbers.append(mu + sigma * z)


    
    def randomFromRejectionMethod(self):
        mu = self.params['mu']
        sigma = self.params['sigma']
        while True:
            u1 = self.rng.random()
            u2 = self.rng.random()
            y1 = - math.log(u1)
            y2 = - math.log(u2)
      
            aux = (y1 - 1)**2 / 2
            if (y2 >= aux):
                abs_z = y1
                z = abs_z if self.rng.random() >= 0.5 else -abs_z
                x = sigma * z + mu
                self.rejection_method_generated_numbers.append(x)
                break

