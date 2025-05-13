from generators.generator import Generator
from generators.linear_congruential_generator import LinearCongruentialGenerator
from generators.quadratic_congruential_generator import QuadraticCongruentialGenerator
import random

class MixedGenerator(Generator):
    order =  0
    def __init__(self, seed: int):
        self.seed = seed
        random.seed(seed)

    instance = None
    @classmethod
    def get_instance(cls, seed:int=3849):
        if cls.instance is None:
            cls.instance = cls(seed)
        return cls.instance

    def update_seed(self, num):
        self.seed = int(num * 10000)

    def random(self):
        match(self.order%3):
            case 0:
                generator = random
            case 1:
                generator = QuadraticCongruentialGenerator.get_instance(self.seed)
            case 2:
                generator = LinearCongruentialGenerator.get_instance(self.seed) 
        
        self.order += 1
        value = generator.random()
        self.update_seed(value)
        return value
