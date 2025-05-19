import math
import numpy as np
from scipy.stats import gamma
from distributions.distribution import Distribution

class GammaDistribution(Distribution):
    dist_name = "gamma"
    dist_type = "continuous"

    def __init__(self, alpha: float, beta: float = 1, seed: int = 12345):
        super().__init__(seed)
        self.params = {"alpha": alpha, "beta": beta}
        
    @classmethod
    def get_instance(cls, alpha: float, beta: float = 1):
        if cls.instance is None:
            cls.instance = cls(alpha,beta)
        return cls.instance


    def getParams(self):
        return self.params

    def get_expected_pdf(self):
        alpha = self.params["alpha"]
        beta = self.params["beta"]
        
        max_x = alpha * beta * 3
        x = np.linspace(0, max_x, 1000)
        pdf = gamma.pdf(x, alpha, scale=1/beta)
        
        return x, pdf


    def randomFromRejectionMethod(self):
        alpha = self.params['alpha']
        beta = self.params['beta']
        if alpha < 1:
            while True:
                u = self.rng.random()
                v = self.rng.random()
                x = (-math.log(u)) ** (1 / alpha)
                y = math.exp(-x)
                if v <= y:
                    self.rejection_method_generated_numbers.append(x / beta)
                    break
        else:
            d = alpha - 1/3
            c = 1 / math.sqrt(9 * d)

            while True:
                z = self.rng.gauss(0, 1)
                u = self.rng.random()
                v = (1 + c * z) ** 3

                if v > 0 and math.log(u) < (0.5 * z**2 + d - d * v + d * math.log(v)):
                    self.rejection_method_generated_numbers.append(d * v / beta)
                    break
        