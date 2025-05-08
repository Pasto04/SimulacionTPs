from generators.generator import Generator

class LinearCongruentialGenerator(Generator):
    def __init__(self, seed: int):
        self.seed = seed
        self.divider = 2**32
        self.multiplier = 1013904223
        self.increase = 1664525

    instance = None

    @classmethod
    def get_instance(cls, seed:int=456):
        if cls.instance is None:
            cls.instance = cls(seed)
        return cls.instance


    def random(self):
        self.seed = (self.multiplier * self.seed + self.increase) % self.divider
        return self.seed / self.divider
