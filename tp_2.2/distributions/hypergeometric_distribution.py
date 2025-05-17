import math
from distributions.distribution import Distribution
class HypergeometricDistribution(Distribution):
    dist_name = "hypergeometric"
    def __init__(self, N: int, K: int, n: int, seed: int = 12345):
        super().__init__(seed)
        self.params = {"N": N, "K": K, "n": n}
        self.rejection_method_generated_numbers = []
    
    def getDistName(self):
        return self.dist_name
    
    def getParams(self):
        return self.params

    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers
        
    @classmethod
    def get_instance(cls, N: int, K: int, n: int):
        if cls.instance is None:
            cls.instance = cls(N, K, n)
        return cls.instance

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

    
    def randomFromRejectionMethod(self) -> int:
        N = self.params['N']
        K = self.params['K']
        n = self.params['n']
        
        x_min = max(0, n - (N - K))  # minimo valor posible de exitos
        x_max = min(n, K)            # maximo valor posible de exitos

        max_pmf = max(self.pmf(N, K, n, x) for x in range(x_min, x_max + 1))

        while True:
            x = self.rng.randint(x_min, x_max)
            y = self.rng.uniform(0, max_pmf)
            fx = self.pmf(N, K, n, x)
            if y <= fx:
                self.rejection_method_generated_numbers.append(x)
                break
