from generators.generator import Generator

class QuadraticCongruentialGenerator(Generator):
    def __init__(self, seed: int):
        self.seed = seed
        self.divider = 2**31 - 1
        self.multiplier = 1103515245
        self.increase = 12345

    instance = None

    @classmethod
    def get_instance(cls, seed:int=795489):
        if cls.instance is None:
            cls.instance = cls(seed)
        return cls.instance


    def random(self):
        self.seed = (self.multiplier * self.seed**2 + self.increase) % self.divider
        return self.seed / self.divider
