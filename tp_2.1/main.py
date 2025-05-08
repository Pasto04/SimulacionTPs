import matplotlib.pyplot as plt
import random
from generators.middle_square_method import MiddleSquareMethod
from generators.linear_congruential_generator import LinearCongruentialGenerator
from generators.quadratic_congruential_generator import QuadraticCongruentialGenerator


def generate_scatter_plot(data, title, x_axys_label, y_axys_label):
    plt.title(title)
    plt.xlabel(x_axys_label)
    plt.ylabel(y_axys_label)

    x_data = list(range(len(data)))
    plt.scatter(x_data, data, color='blue', marker='o', s=10)
    plt.show()


def main():
    middle_square_generator = MiddleSquareMethod.get_instance()
    linear_generator = LinearCongruentialGenerator.get_instance()
    quadratic_generator = QuadraticCongruentialGenerator.get_instance()
    python_generator = random

    generated_numbers = {
        "middle_square_generator":[],
        "linear_generator":[],
        "quadratic_generator":[],
        "python_generator":[]
    }


    #TODO cuántos nros hay que generar para los tests? @joaquin
    for x in range (1000):
        generated_numbers['middle_square_generator'].append(middle_square_generator.random())
        generated_numbers['linear_generator'].append(linear_generator.random())
        generated_numbers['quadratic_generator'].append(quadratic_generator.random())
        generated_numbers['python_generator'].append(python_generator.random())



    generate_scatter_plot(generated_numbers['middle_square_generator'], "Generador Medios Cuadrados", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['linear_generator'], "Generador Lineal Congruencial", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['quadratic_generator'], "Generador Cuadrático Congruencial", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['python_generator'], "Generador Lenguaje Python", "Índice", "Valor")
    #TODO se debe testear con al menos cuatro pruebas para determinar la calidad de generación.


if __name__ == "__main__":
    main()
