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
        
        # Explicación según si pasa el test o no
        if passed:
            print(f"¿Pasa el test? Sí\nExplicación: El valor calculado del Chi-cuadrado es menor que el valor crítico, lo que indica que los números generados tienen una distribución uniforme. El generador pasa el test de frecuencia.")
        else:
            print(f"¿Pasa el test? No\nExplicación: El valor calculado del Chi-cuadrado es mayor que el valor crítico, lo que indica que los números generados no tienen una distribución uniforme. El generador no pasa el test de frecuencia debido a sesgos en la generación de números aleatorios.")

    
     # Test de independencia de runs
        runs_count, runs_expected, runs_passed = runs_test(numbers)
        print(' ')
        print(f"{name.upper()} - Test de Independencia de Runs:")
        print(f"Cantidad de corridas observadas: {runs_count}")
        print(f"Cantidad de corridas esperadas: {runs_expected}")
        
        if runs_passed:
            print("¿Pasa el test? Sí\nExplicación: La cantidad de corridas observadas es cercana a la cantidad esperada, lo que indica independencia entre los valores generados.")
        else:
            print("¿Pasa el test? No\nExplicación: La cantidad de corridas observadas es significativamente diferente de la cantidad esperada, lo que indica que los valores generados no son independientes.")



def chi_squared_critical_value(df, alpha=0.05):
    critical_values = {
        1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
        6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
    }
    return critical_values.get(df, None)

def frequency_test(random_numbers, num_intervals=10, alpha=0.05):
    n = len(random_numbers)
    expected_freq = n / num_intervals
    observed_freqs = [0] * num_intervals

    for number in random_numbers:
        index = min(int(number * num_intervals), num_intervals - 1)
        observed_freqs[index] += 1

    chi_squared = sum(
        (obs - expected_freq) ** 2 / expected_freq
        for obs in observed_freqs
    )

    critical_value = chi_squared_critical_value(num_intervals - 1, alpha)
    passed = chi_squared < critical_value if critical_value else False
    return chi_squared, critical_value, passed

def runs_test(random_numbers):
    median = sorted(random_numbers)[len(random_numbers) // 2]  # Mediana empírica
    signs = [1 if x >= median else 0 for x in random_numbers]
    
    runs = 1
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]:
            runs += 1

    n1 = signs.count(1)
    n2 = signs.count(0)
    n = n1 + n2

    if n1 < 0 or n2 < 0:
        return runs, None, False  # No se puede aplicar el test

    expected_runs = (2 * n1 * n2) / n + 1
    variance_runs = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))
    z = (runs - expected_runs) / (variance_runs ** 0.5)

    passed = abs(z) < 1.96  # Nivel de confianza del 95%
    return runs, expected_runs, passed

if __name__ == "__main__":
    main()
