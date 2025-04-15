"""
Roulette Simulator:
Dev Team:
    - Cosentino, Lucio Nahuel
    - Danteo, Elías Tomás
    - De Bernardo, Aarón
    - Fernandez Da Silva, Joaquín C.
    - Malizani, Juan Pablo
    - Pastorino, Juan José
"""

import random
import matplotlib.pyplot as plt
import argparse
import numpy as np #np.mean() -> promedio np.var() -> varianza np.std -> desvio
import math

chosen_number = number_of_spins = number_of_batches = 0
expected_values = {
    'frequency': 1 / 37,  # 1/37 porque hay 37 números en la ruleta
    'mean': 18,  # (0 + 36) / 2 = 18, así se calcula el promedio de la distribución uniforme
    'variance': ((36 - 0 + 1) ** 2 - 1) / 12,  # varianza de la distribución uniforme
    'std': math.sqrt(((36 - 0 + 1) ** 2 - 1) / 12)  # desviación estándar de la distribución uniforme
}

def get_simulation_args():
    global chosen_number
    global number_of_spins
    global number_of_batches
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", help="Valor del numero de corridas (15 por defecto)", default=5)
    parser.add_argument("-t", "--tiradas", help="Valor del numero de tiradas por corrida (500 por defecto)", default=100)
    parser.add_argument("-n", "--numero", help="Valor del numero a analizar (7 por defecto)", default=7)

    args, unknown = parser.parse_known_args()
    number_of_batches = int(args.corridas)
    number_of_spins = int(args.tiradas)
    chosen_number = int(args.numero)
    print(f"Ejecutando {str(number_of_batches)} corridas de {str(number_of_spins)} tiradas para el número {str(chosen_number)}.")


def generate_batch(number_of_spins: int): # numeros que salieron en c/u de las n tiradas del batch
    return [random.randint(0, 36) for _ in range(number_of_spins)]


def calculate_batch_statistics(result_batch, chosen_number, batch_number, array_results_history):
    for a in range(1, len(result_batch)):  
        count = result_batch[0:a].count(chosen_number)
        relative_frequency = count / a

        batch_mean = np.mean(result_batch[0:a])
        batch_variance = np.var(result_batch[0:a])
        batch_std = np.std(result_batch[0:a])

        array_results_history[batch_number]['frequency'].append(relative_frequency)
        array_results_history[batch_number]['mean'].append(batch_mean)
        array_results_history[batch_number]['variance'].append(batch_variance)
        array_results_history[batch_number]['std'].append(batch_std)


def generate_subplot(title, subplot_number, x_axys_label, y_axys_label, data, expected_value):
    plt.subplot(2, 2, subplot_number)
    plt.title(title)
    plt.xlabel(x_axys_label)
    plt.ylabel(y_axys_label)

    list.insert(0, 0)  
    plt.xlim(1, number_of_spins + 1)
    plt.plot(list, label="Valor obtenido")

    puntosX = np.array([1, number_of_spins])
    puntosY = np.array([expected_value, expected_value])
    plt.plot(puntosX, puntosY, label="Valor esperado")
    
    plt.legend()
    plt.plot()


def plot_batch_statistics(batch_number, array_results_history, expected_values):
    generate_subplot("Frecuencia Relativa", 1, "Número de tirada", "Frecuencia relativa", array_results_history[batch_number]["frequency"], expected_values["frequency"])
    generate_subplot("Promedio", 2, "Número de tirada", "Valor promedio", array_results_history[batch_number]["mean"], expected_values["mean"])
    generate_subplot("Varianza", 3, "Número de tirada", "Valor de la varianza", array_results_history[batch_number]["variance"], expected_values["variance"])
    generate_subplot("Desvío Estándar", 4, "Número de tirada", "Valor del desvío", array_results_history[batch_number]["std"], expected_values["std"])
    
    plt.suptitle(f"CORRIDA NÚMERO {batch_number+1}")
    fig_manager = plt.get_current_fig_manager()
    fig_manager.resize(1366, 768)
    plt.tight_layout()
    plt.show()


def run_simulation_batches(array_results_history):
    for batch_number in range(number_of_batches):
        result_batch = generate_batch(number_of_spins)
        calculate_batch_statistics(result_batch, chosen_number, batch_number, array_results_history)
        plot_batch_statistics(batch_number, array_results_history, expected_values)


def main():
    get_simulation_args()  
    
    array_results_history = [{
        'frequency': [],
        'mean': [],
        'variance': [],
        'std': []
    } for _ in range(number_of_batches)] 

    run_simulation_batches(array_results_history)  

# Arranca el Programa
if __name__ == "__main__":
    main()

