from generators.middle_square_method import MiddleSquareMethod
from generators.lineal_congruential_generator import LinearCongruentialGenerator
from generators.quadratic_congruential_generator import QuadraticCongruentialGenerator

generator = QuadraticCongruentialGenerator.get_instance()

for x in range (100):
    print(generator.random())
