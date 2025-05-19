import math
from distributions.distribution import Distribution
class ExponentialDistribution(Distribution):
    dist_name = "exponential"

    def __init__(self, lambda_: float, seed:int =12345):
        super().__init__(seed)
        self.params = {"lambda": lambda_}
        self.rejection_method_generated_numbers = []
        self.inverse_transform_generated_numbers = []

    def getDistName(self):
        return self.dist_name
    
    def getParams(self):
        return self.params

    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers

    def getInverseTransformGeneratedNumbers(self):
        return self.inverse_transform_generated_numbers
        
    @classmethod
    def get_instance(cls, lambda_: float):
        if cls.instance is None:
            cls.instance = cls(lambda_)
        return cls.instance
    
    
    def randomFromInverseTransform(self):
        lambda_ = self.params['lambda']
        r = self.rng.random()
        x = - (1 / lambda_) * math.log(r)
        self.inverse_transform_generated_numbers.append(x)

    def randomFromRejectionMethod(self):
        lambda_ = self.params['lambda']
        x_max = -math.log(0.0001) / lambda_ 
        y_max = lambda_       

        while True:
            x = self.rng.uniform(0, x_max)
            y = self.rng.uniform(0, y_max)
            fx = lambda_ * math.exp(-lambda_ * x)
            if y <= fx:
                self.rejection_method_generated_numbers.append(x)
                break

