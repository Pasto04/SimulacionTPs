from abc import ABC, abstractmethod
class Distribution:
    inverse_transform_generated_numbers = []
    rejection_method_generated_numbers = []
    instance = None
    dist_name = None
    params = {}
    def __init__(self):
        pass

    def getDistName(self):
        return self.dist_name
    
    def getParams(self):
        return self.params

    def getRejectionMethodGeneratedNumbers(self):
        return self.rejection_method_generated_numbers

    def getInverseTransformGeneratedNumbers(self):
        return self.inverse_transform_generated_numbers
    @classmethod
    def get_instance(cls):
        pass
    
    @classmethod
    def randomFromRejectionMethod(cls):
        pass

    @classmethod
    def randomFromInverseTransform(cls):
        pass