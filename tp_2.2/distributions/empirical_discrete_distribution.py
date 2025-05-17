import random
import matplotlib.pyplot as plt
import numpy as np
from distributions.distribution import Distribution
class EmpiricalDiscreteDistribution(Distribution):
    dist_name = "empirical_discrete"
    def __init__(self, values: int, probs: float):
        EmpiricalDiscreteDistribution.params = {"values": values, "probs": probs}

    @classmethod
    def get_instance(cls, values: int, probs: float):
        if cls.instance is None:
            cls.instance = cls(values, probs)
        return cls.instance

    @classmethod
    def randomFromRejectionMethod(cls):
        values = cls.params['values']
        probs = cls.params['probs']
        if not values or not probs or len(values) != len(probs):
            raise ValueError("Values and probs must be non-empty lists of the same length.")

        max_prob = max(probs)
        while True:
            idx = random.randint(0, len(values) - 1)
            u = random.uniform(0, max_prob)
            if u <= probs[idx]:
                cls.rejection_method_generated_numbers.append(values[idx])
                break