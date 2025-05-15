import math
import random

class HypergeometricDistribution:
    @staticmethod
    def pmf(N: int, K: int, n: int, x: int) -> float:
        # N = tamaño de la población
        # K = número de éxitos en la población
        # n = número de extracciones
        # x = número de éxitos en las extracciones
        #calculo la probabilidad de obtener exactamente x exitos al extraer n elementos
        #sin reposicion de una población de tamaño N con K exitos posibles.
        
        if x < 0 or x > K or x > n or n - x > N - K:
            return 0.0
        return (math.comb(K, x) * math.comb(N - K, n - x)) / math.comb(N, n)

    @classmethod
    def randomFromRejectionMethod(cls, N: int, K: int, n: int) -> int:
        #genera un numero aleatorio con distribucion hipergeometrica usando el metodo de rechazo.
        
        x_min = max(0, n - (N - K))  # minimo valor posible de exitos
        x_max = min(n, K)            # maximo valor posible de exitos

        max_pmf = max(cls.pmf(N, K, n, x) for x in range(x_min, x_max + 1))

        while True:
            x = random.randint(x_min, x_max)
            y = random.uniform(0, max_pmf)
            fx = cls.pmf(N, K, n, x)
            if y <= fx:
                return x
