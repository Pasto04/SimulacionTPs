import math
import random
import matplotlib.pyplot as plt
import numpy as np

class BinomialDistribution:
    @classmethod
    def random_from_rejection_method(cls, n: int, p: float) -> int:
        x_max = n
        max_pmf = max(math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(n + 1))
        y_max = max_pmf

        while True:
            x = random.randint(0, x_max)
            y = random.uniform(0, y_max)
            fx = math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
            if y <= fx:
                return x


