import math
import random

class ExponentialDistribution:
    @classmethod
    def randomFromInverseTransform(cls, lambda_: float):
        r = random.random()
        return - (1 / lambda_) * math.log(r)


    @classmethod
    def randomFromRejectionMethod(cls, lambda_: float):
        x_max = -math.log(0.0001) / lambda_ 
        y_max = lambda_       

        while True:
            x = random.uniform(0, x_max)
            y = random.uniform(0, y_max)
            fx = lambda_ * math.exp(-lambda_ * x)
            if y <= fx:
                return x

