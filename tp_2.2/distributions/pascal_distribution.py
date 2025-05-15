import math
import random

class PascalDistribution:
    @staticmethod
    def pmf(r: int, p: float, x: int) -> float:
        # r = cantidad de exitos a lograr
        # p = probabilidad de exito en cada ensayo (entre 0 y 1)
        # x = cantidad de fracasos
        #funcion de masa de probabilidad de Pascal (binomial negativa).
        #P(X = x) = C(x + r - 1, x) * (1 - p)^x * p^r
        if x < 0 or r <= 0 or not (0 < p < 1):
            return 0.0
        return math.comb(x + r - 1, x) * ((1 - p) ** x) * (p ** r)

    @classmethod
    def randomFromRejectionMethod(cls, r: int, p: float) -> int:
        
        #genera un numero aleatorio con distribucion Pascal (binomial negativa) usando metodo de rechazo.
        
        if r <= 0 or not (0 < p < 1):
            return 0

        # dominio razonable: los valores mas probables estan cerca de la media
        # valor esperado: r * (1 - p) / p
        media = r * (1 - p) / p
        desvio = math.sqrt(r * (1 - p) / (p ** 2))
        x_max = int(media + 10 * desvio)
        max_pmf = max(cls.pmf(r, p, x) for x in range(0, x_max + 1))

        while True:
            x = random.randint(0, x_max)
            y = random.uniform(0, max_pmf)
            fx = cls.pmf(r, p, x)
            if y <= fx:
                return x
