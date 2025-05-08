from abc import ABC, abstractmethod

class Generator(ABC):
    def __init__(self):
        self.seed = None

    def set_seed(self, new_seed):
        self.seed = new_seed

    @abstractmethod
    def random():
        pass
