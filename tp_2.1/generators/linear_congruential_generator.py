from generators.generator import Generator

class LinearCongruentialGenerator(Generator):
    def __init__(self, seed: int):
        self.seed = seed
        self.divider = 2**48
        self.multiplier = 25214903917
        self.increase = 11

    instance = None

    @classmethod
    def get_instance(cls, seed:int=1532):
        if cls.instance is None:
            cls.instance = cls(seed)
        return cls.instance


    def random(self):
        self.seed = (self.multiplier * self.seed + self.increase) % self.divider
        return self.seed / self.divider
