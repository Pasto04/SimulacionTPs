from distributions.distribution import Distribution
class UniformDistribution(Distribution):
    dist_name = "uniform"
    def __init__(self, a: float, b: float, seed: int = 12345):
        super().__init__(seed)
        self.params = {"a": a, "b": b}
        self.rejection_method_generated_numbers = []
        self.inverse_transform_generated_numbers = []
        
    @classmethod
    def get_instance(cls, a: float, b: float):
        if cls.instance is None:
            cls.instance = cls(a,b)
        return cls.instance
    
    def getDistName(self):
        return self.dist_name
    
    def getParams(self):
        return self.params

    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers
    
    def getInverseTransformGeneratedNumbers(self):
        return self.inverse_transform_generated_numbers
    
    
    def randomFromInverseTransform(self):
        a = self.params['a']
        b = self.params['b']
        r = self.rng.random()
        x= a + (b-a) * r
        self.inverse_transform_generated_numbers.append(x)


    
    def randomFromRejectionMethod(self):
        a = self.params['a']
        b = self.params['b']
        c = a - (b - a)
        d = b + (b - a)
        aceptacion = (b - a) / (d - c)

        while True:
            y = c + (d - c) * self.rng.random()
            u = self.rng.random()
            if a <= y <= b and u < aceptacion:
                self.rejection_method_generated_numbers.append(y)
                break

