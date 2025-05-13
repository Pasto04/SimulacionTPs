from generators.generator import Generator

class MiddleSquareMethod(Generator):
    
    def __init__(self, seed: int):
        self.seed = seed

    instance = None
    @classmethod
    def get_instance(cls, seed:int=9731):
        if cls.instance is None:
            cls.instance = cls(seed)
        return cls.instance
    
    def getCoreValues(self, num) -> int:
        str_number = str(num)
        length = len(str_number)
        
        if length < 4:
            return str_number
        
        start_index = length // 2 - 2
        end_index = start_index + 4
        
        number = int(str_number[start_index:end_index])
        return number


    def random(self):
        value = self.seed**2
        value = str(value).zfill(8) # agrega ceros al inicio si hay menos de 8 digitos

        self.seed = self.getCoreValues(value)
        return float('0.' + str(self.seed))
