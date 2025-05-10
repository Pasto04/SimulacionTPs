import matplotlib.pyplot as plt
import random
from generators.middle_square_method import MiddleSquareMethod
from generators.linear_congruential_generator import LinearCongruentialGenerator
from generators.quadratic_congruential_generator import QuadraticCongruentialGenerator

from tests import frequency_test, runs_test, reverse_arrangements_test, overlapping_sums_test, binary_rank_test

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
        "middle_square_generator": [],
        "linear_generator": [],
        "quadratic_generator": [],
        "python_generator": []
    }

    #TODO cuántos nros hay que generar para los tests? @joaquin (lo voy a hacer en base a los test, despues me encargo de agregarlo también al informe)
    for x in range(1000):
        generated_numbers['middle_square_generator'].append(middle_square_generator.random())
        generated_numbers['linear_generator'].append(linear_generator.random())
        generated_numbers['quadratic_generator'].append(quadratic_generator.random())
        generated_numbers['python_generator'].append(python_generator.random())

    generate_scatter_plot(generated_numbers['middle_square_generator'], "Generador Medios Cuadrados", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['linear_generator'], "Generador Lineal Congruencial", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['quadratic_generator'], "Generador Cuadrático Congruencial", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['python_generator'], "Generador Lenguaje Python", "Índice", "Valor")
    #TODO se debe testear con al menos cuatro pruebas para determinar la calidad de generación.

    for name, numbers in generated_numbers.items():
        chi, critical, passed = frequency_test(numbers)
        print(f"\n{name.upper()} - Test de Frecuencia (Chi-cuadrado):")
        print(f"Chi-cuadrado calculado: {chi:.4f}")
        print(f"Valor crítico (α=0.05): {critical:.4f}")
        if passed:
            print("¿Pasa el test? Sí")
            print("Explicación: el valor calculado es menor que el crítico; la distribución es uniforme.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: el valor calculado supera el crítico; la distribución no es uniforme.")

        runs_count, runs_expected, runs_passed = runs_test(numbers)
        print(f"\n{name.upper()} - Test de Independencia de Corridas:")
        print(f"Corridas observadas: {runs_count}")
        print(f"Corridas esperadas: {runs_expected:.2f}")
        if runs_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: las corridas observadas coinciden con las esperadas; hay independencia.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: las corridas observadas difieren significativamente; falta independencia.")

        inv_count, inv_expected, inv_passed = reverse_arrangements_test(numbers)
        print(f"\n{name.upper()} - Test de Arreglos Inversos:")
        print(f"Inversiones observadas: {inv_count}")
        print(f"Inversiones esperadas: {inv_expected:.2f}")
        if inv_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: el número de inversiones está dentro del rango esperado.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: el número de inversiones está fuera del rango esperado; posible sesgo.")

        sum_stat, sum_expected, sum_passed = overlapping_sums_test(numbers)
        print(f"\n{name.upper()} - Test de Sumas Solapadas (m=5):")
        print(f"Suma media observada: {sum_stat:.4f}")
        print(f"Suma media esperada: {sum_expected:.4f}")
        if sum_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: la media de las sumas concuerda con la teórica; cumple iid.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: la media de las sumas difiere; posible dependencia o sesgo.")

        rank_dist, rank_passed = binary_rank_test(numbers)
        print(f"\n{name.upper()} - Test de Rango Binario (32×32):")
        print(f"Distribución de rangos: {rank_dist}")
        if rank_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: la distribución de rangos coincide con las proporciones teóricas.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: la distribución de rangos difiere de la esperada; posibles fallos.")

if __name__ == "__main__":
    main()
