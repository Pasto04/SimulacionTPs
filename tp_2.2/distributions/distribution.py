from abc import ABC, abstractmethod
import random
class Distribution:
    instance = None
    dist_name = None
    
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


    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers
    

    def getInverseTransformGeneratedNumbers(self):
        return self.inverse_transform_generated_numbers
    
    
    def randomFromRejectionMethod(self):
        pass

    
    def randomFromInverseTransform(self):
        pass