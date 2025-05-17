import random
from distributions.distribution import Distribution
class UniformDistribution(Distribution):
    dist_name = "uniform"
    def __init__(self, a: float, b: float):
        UniformDistribution.params = {"a": a, "b": b}
        
    @classmethod
    def get_instance(cls, a: float, b: float):
        if cls.instance is None:
            cls.instance = cls(a,b)
        return cls.instance
    
    @classmethod
    def randomFromInverseTransform(cls):
        a = cls.params['a']
        b = cls.params['b']
        r = random.random()
        x= a + (b-a) * r
        cls.inverse_transform_generated_numbers.append(x)


    @classmethod
    def randomFromRejectionMethod(cls):
        a = cls.params['a']
        b = cls.params['b']
        c = a - (b - a)
        d = b + (b - a)
        aceptacion = (b - a) / (d - c)

        while True:
            y = c + (d - c) * random.random()
            u = random.random()
            if a <= y <= b and u < aceptacion:
                cls.rejection_method_generated_numbers.append(y)
                break

