from abc import ABC
import random

class Distribution(ABC):
    instance = None
    dist_name = None
    dist_type = None
    
    def __init__(self,seed=12345):
        self.rng = random.Random(seed)
        self.params = {}
        self.rejection_method_generated_numbers = []
        self.inverse_transform_generated_numbers = []

    @classmethod
    def get_instance(cls):
        pass

    @classmethod
    def get_params(cls):
        pass

    @classmethod
    def get_dist_name(cls):
        return cls.dist_name

    @classmethod
    def get_dist_type(cls):
        return cls.dist_type

    def randomFromRejectionMethod(self):
        pass
    
    def randomFromInverseTransform(self):
        pass

    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers

    def getInverseTransformGeneratedNumbers(self):
        return  self.inverse_transform_generated_numbers
