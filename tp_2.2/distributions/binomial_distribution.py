import math

import matplotlib.pyplot as plt
import numpy as np
from distributions.distribution import Distribution
class BinomialDistribution(Distribution):
    dist_name = "binomial"
    def __init__(self, n: int, p: float, seed=12345):
        super().__init__(seed)
        #n: Número de ensayos
        #p: Probabilidad de éxito en cada ensayo
        self.params = {"n": n, "p": p}
        self.rejection_method_generated_numbers = []

    def getDistName(self):
        return self.dist_name
    
    def getParams(self):
        return self.params

    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers

    
    
    @classmethod
    def get_instance(cls, n: int, p: float):
        if cls.instance is None:
            cls.instance = cls(n, p)
        return cls.instance
    
    
    def randomFromRejectionMethod(self):
        n = self.params['n']
        p = self.params['p']
        x_max = n
        max_pmf = max(math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(n + 1))
        y_max = max_pmf

        while True:
            x = self.rng.randint(0, x_max)
            y = self.rng.uniform(0, y_max)
            fx = math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
            if y <= fx:
                self.rejection_method_generated_numbers.append(x)
                break

