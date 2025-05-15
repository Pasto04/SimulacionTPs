import random

class UniformDistribution:
    @classmethod
    def randomFromInverseTransform(cls, a: float, b: float):
        r = random.random()
        return a + (b-a) * r


    @classmethod
    def randomFromRejectionMethod(cls, a: float, b: float):
        c = a - (b - a)
        d = b + (b - a)
        aceptacion = (b - a) / (d - c)

        while True:
            y = c + (d - c) * random.random()
            u = random.random()
            if a <= y <= b and u < aceptacion:
                return y

