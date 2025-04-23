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
from entities.strats import FibbonaciStrat, MartingalaStrat, DAlembertStrat, ParoliStrat
from entities.player import Player
from entities.roulette import Roulette



def get_simulation_args():
    global chosen_bet
    global number_of_spins
    global number_of_batches
    global chosen_strat
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tiradas", help="Valor del número de tiradas por corrida (415 por defecto)", default=415)
    parser.add_argument('-c', '--corridas', default=15, type=int, help='Valor del número de corridas (Por defecto: %(default)s)')
    parser.add_argument('-n', '--seleccion', default='rojo', type=tipoSeleccion, help="Selección: un número, \"rojo\", \"negro\", \"par\", \"impar\", \"docena1\", \"docena2\", \"docena3\", \"col1\", \"col2\", \"col3\" (Por defecto: %(default)s)")
    parser.add_argument('-s', '--estrategia', default='m', choices=['m','d','f','p'], help="Estrategia a utilizar: \"m\" - Martingala, \"d\" - D'Alemnert, \"f\" - Fibonacci, \"p\" - Paroli (Por defecto: %(default)s)", )
    parser.add_argument('-a', '--capital', default=30000, type=tipoCapital, help="Capital: \"i\" para infinito o el monto si es finito (Por defecto: %(default)s - Mínimo 1000)")

    args, unknown = parser.parse_known_args()
    number_of_batches = int(args.corridas)
    number_of_spins = int(args.tiradas)
    chosen_bet = int(args.seleccion)
    chosen_strat = args.estrategia
    capital_limit = args.capital
    


    print(f"Ejecutando {str(number_of_batches)} corridas de {str(number_of_spins)} tiradas para el número {str(chosen_number)}.")

    
    player = Player(12)
    strat = None
    
    match(chosen_strat):
        case 'm': strat = MartingalaStrat(1, 12)
        case 'd': strat = DAlembertStrat(1, 12)
        case 'o': strat = ParoliStrat(1, 12)
        case 'f': strat = FibbonaciStrat(1, 12)

    while True:
        try:
            pass
        except ValueError as e:
            print(e)