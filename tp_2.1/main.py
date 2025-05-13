import matplotlib.pyplot as plt
import random
from tabulate import tabulate
from generators.middle_square_method import MiddleSquareMethod
from generators.linear_congruential_generator import LinearCongruentialGenerator
from generators.quadratic_congruential_generator import QuadraticCongruentialGenerator
from generators.mixed_generator import MixedGenerator   

from tests import Tests

def generate_scatter_plot(data, title, x_axys_label, y_axys_label):
    plt.title(title)
    plt.xlabel(x_axys_label)
    plt.ylabel(y_axys_label)

    x_data = list(range(len(data)))
    plt.scatter(x_data, data, color='blue', marker='o', s=10)
    plt.show()

def generate_comparison_table(results):
    headers = ["Generador", "Frecuencia", "Corridas", "Arreglos Inversos", "Sumas superpuestas", "Poker"]
    table_data = []
    for name, tests in results.items():
        row = [
            name.replace("_", " ").title(),
            "✓" if tests["frequency_test"] else "X",
            "✓" if tests["runs_test"] else "X",
            "✓" if tests["reverse_arrangements_test"] else "X",
            "✓" if tests["overlapping_sums_test"] else "X",
            "✓" if tests["poker_test"] else "X",
        ]
        table_data.append(row)
    print( "✓: Pasó el test - X: No pasó el test")
    print(tabulate(table_data, headers, tablefmt= 'grid'))


def main():
    middle_square_generator = MiddleSquareMethod.get_instance()
    linear_generator = LinearCongruentialGenerator.get_instance()
    quadratic_generator = QuadraticCongruentialGenerator.get_instance()
    mixed_generator = MixedGenerator.get_instance()
    python_generator = random
    

    generated_numbers = {
        "middle_square_generator": [],
        "linear_generator": [],
        "quadratic_generator": [],
        "python_generator": [],
        "mixed_generator": []
    }

    for _ in range(3207):
        generated_numbers['middle_square_generator'].append(middle_square_generator.random())
        generated_numbers['linear_generator'].append(linear_generator.random())
        generated_numbers['quadratic_generator'].append(quadratic_generator.random())
        generated_numbers['mixed_generator'].append(mixed_generator.random())

    python_generator.seed(5487)
    for _ in range(3207):
        generated_numbers['python_generator'].append(python_generator.random())

    testPassed = {
        "frequency_test": bool,
        "runs_test": bool,
        "reverse_arrangements_test": bool,
        "overlapping_sums_test": bool,
        'poker_test' : bool,
    }
    testsPassedByGenerator = {
        "middle_square_generator": testPassed.copy(),
        "linear_generator": testPassed.copy(),
        "quadratic_generator": testPassed.copy(),
        "python_generator": testPassed.copy(),
        "mixed_generator": testPassed.copy()
    }


    for name, numbers in generated_numbers.items():
        chi, critical, frequency_test_passed = Tests.frequency_test(numbers)
        testsPassedByGenerator[name]["frequency_test"] = frequency_test_passed
        print(f"\n{name.upper()} - Test de Frecuencia (Chi-cuadrado):")
        print(f"Chi-cuadrado calculado: {chi:.4f}")
        print(f"Valor crítico (α=0.05): {critical:.4f}")
        if frequency_test_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: el valor calculado es menor que el crítico; la distribución es uniforme.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: el valor calculado supera el crítico; la distribución no es uniforme.")

        runs_test_count, runs_test_expected, runs_test_passed = Tests.runs_test(numbers)
        testsPassedByGenerator[name]["runs_test"] = runs_test_passed
        print(f"\n{name.upper()} - Test de Independencia de Corridas:")
        print(f"Corridas observadas: {runs_test_count}")
        print(f"Corridas esperadas: {runs_test_expected:.2f}")
        if runs_test_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: las corridas observadas coinciden con las esperadas; hay independencia.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: las corridas observadas difieren significativamente; falta independencia.")

        inv_test_count, inv_test_expected, inv_test_passed = Tests.reverse_arrangements_test(numbers)
        testsPassedByGenerator[name]["reverse_arrangements_test"] = inv_test_passed
        print(f"\n{name.upper()} - Test de Arreglos Inversos:")
        print(f"Inversiones observadas: {inv_test_count}")
        print(f"Inversiones esperadas: {inv_test_expected:.2f}")
        if inv_test_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: el número de inversiones está dentro del rango esperado.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: el número de inversiones está fuera del rango esperado; posible sesgo.")

        sum_test_stat, sum_test_expected, sum_test_passed = Tests.overlapping_sums_test(numbers)
        testsPassedByGenerator[name]["overlapping_sums_test"] = sum_test_passed
        print(f"\n{name.upper()} - Test de Sumas Solapadas (m=5):")
        print(f"Suma media observada: {sum_test_stat:.4f}")
        print(f"Suma media esperada: {sum_test_expected:.4f}")
        if sum_test_passed:
            print("¿Pasa el test? Sí")
            print("Explicación: la media de las sumas concuerda con la teórica; cumple iid.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: la media de las sumas difiere; posible dependencia o sesgo.")
        
        
        #TEST DE POKER
        poker_result = Tests.poker_test(numbers)
        testsPassedByGenerator[name]["poker_test"] = poker_result["passed"]
        
        print(f"\n{name.upper()} - Test de Poker:")
        print(f"Frecuencia de todos diferentes: {poker_result['patterns']['Todos diferentes']}")
        print(f"Frecuencia de pares: {poker_result['patterns']['Un par']}")
        print(f"Frecuencia de dos pares: {poker_result['patterns']['Dos pares']}")
        print(f"Frecuencia de trios: {poker_result['patterns']['Trio']}")
        print(f"Frecuencia de full: {poker_result['patterns']['Full']}")
        print(f"Frecuencia de poker: {poker_result['patterns']['Poker']}")
        print(f"Frecuencia de quintilla: {poker_result['patterns']['Quintilla']}")
        
        if poker_result["passed"]:
            print("¿Pasa el test? Sí")
            print("Explicación: la frecuencia de combinaciones es consistente con la distribución esperada.")
        else:
            print("¿Pasa el test? No")
            print("Explicación: la frecuencia de combinaciones no es consistente con la distribución esperada; posible sesgo.")
    generate_comparison_table(testsPassedByGenerator)

    generate_scatter_plot(generated_numbers['middle_square_generator'], "Generador Medios Cuadrados", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['linear_generator'], "Generador Lineal Congruencial", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['quadratic_generator'], "Generador Cuadrático Congruencial", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['python_generator'], "Generador Lenguaje Python", "Índice", "Valor")
    generate_scatter_plot(generated_numbers['mixed_generator'], "Generador Mixto", "Índice", "Valor")



if __name__ == "__main__":
    main()
