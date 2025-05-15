import math
import random
class NormalDistribution:
    @classmethod
    def randomFromRejectionMethod(cls, alpha, beta=1):
        if alpha < 1:
            while True:
                u = random.random()
                v = random.random()
                x = (-math.log(u)) ** (1 / alpha)
                y = math.exp(-x)
                if v <= y:
                    return x / beta
        else:
            d = alpha - 1/3
            c = 1 / math.sqrt(9 * d)

            while True:
                z = random.gauss(0, 1)
                u = random.random()
                v = (1 + c * z) ** 3

                if v > 0 and math.log(u) < (0.5 * z**2 + d - d * v + d * math.log(v)):
                    return d * v / beta
        