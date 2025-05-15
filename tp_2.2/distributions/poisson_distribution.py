import math
import random


class PoissonDistribution:
    @classmethod
    def randomFromRejectionMethod(cls, lam: float) -> int:
        if lam <= 0:
            return 0

        b = 0.931 + 2.53 * math.sqrt(lam)
        a = -0.059 + 0.02483 * b
        inv_alpha = 1.1239 + 1.1328 / (b - 3.4)
        vr = 0.9277 - 3.6224 / (b - 2)

        while True:
            u = random.random() - 0.5
            v = random.random()
            us = 0.5 - abs(u)
            k = int(math.floor((2 * a / us + b) * u + lam + 0.43))
            if k < 0:
                continue

            if us >= 0.07 and v <= vr:
                return k

            log_p = -lam + k*math.log(lam) - math.lgamma(k+1)
            log_q = math.log(v * inv_alpha / (us*us))
            if log_q <= log_p:
                return k
