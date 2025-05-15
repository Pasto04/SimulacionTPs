import math
import random
import matplotlib.pyplot as plt
import numpy as np

class EmpiricalDiscreteDistribution:
    @classmethod
    def random_from_rejection_method(cls, values: list, probabilities: list) -> int:
        if not values or not probabilities or len(values) != len(probabilities):
            raise ValueError("Values and probabilities must be non-empty lists of the same length.")

        max_prob = max(probabilities)
        while True:
            idx = random.randint(0, len(values) - 1)
            u = random.uniform(0, max_prob)
            if u <= probabilities[idx]:
                return values[idx]