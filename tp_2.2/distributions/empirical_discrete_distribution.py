import numpy as np
from distributions.distribution import Distribution

class EmpiricalDiscreteDistribution(Distribution):
    dist_name = "empirical_discrete"
    dist_type = "discrete"

    def __init__(self, values: int, probs: float, seed=42):
        super().__init__(seed)
        self.params = {"values": values, "probs": probs}


    def getParams(self):
        return self.params
    
    
    @classmethod
    def get_instance(cls, values: int, probs: float):
        if cls.instance is None:
            cls.instance = cls(values, probs)
        return cls.instance

    def get_expected_pmf(self):
        values = self.params["values"]
        probs = self.params["probs"]
        
        x = np.array(values)
        pmf = np.array(probs)
        
        return x, pmf


    def randomFromRejectionMethod(self):
        values = self.params['values']
        probs = self.params['probs']
        if not values or not probs or len(values) != len(probs):
            raise ValueError("Values and probs must be non-empty lists of the same length.")

        max_prob = max(probs)
        while True:
            idx = self.rng.randint(0, len(values) - 1)
            u = self.rng.uniform(0, max_prob)
            if u <= probs[idx]:
                self.rejection_method_generated_numbers.append(values[idx])
                break