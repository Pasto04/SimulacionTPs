import math
import random

class NormalDistribution:
    @classmethod
    def randomFromInverseTransform(cls, ex = 0, stdx = 1): # en realidad no es por el método de la transformada inversa
        total = 0
        for _ in range(12):
            r = random.random()
            total += r
        z = total - 6

        return ex + stdx * z


    @classmethod
    def randomFromRejectionMethod(cls, ex = 0, stdx = 1):
        while True:
            u1 = random.random()
            u2 = random.random()
            y1 = - math.log(u1)
            y2 = - math.log(u2)
      
            aux = (y1 - 1)**2 / 2
            if (y2 >= aux):
                abs_z = y1
                z = abs_z if random.random() >= 0.5 else -abs_z
                x = stdx * z + ex
                return x

