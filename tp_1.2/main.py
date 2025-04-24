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


chosen_bet = number_of_spins = number_of_batches = initial_capital = 0
chosen_strat = ''


def get_simulation_args():
    global chosen_bet, number_of_spins, number_of_batches, chosen_strat, initial_capital
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tiradas", help="Valor del número de tiradas por corrida (415 por defecto)", default=415)
    parser.add_argument('-c', '--corridas', default=15, type=int, help='Valor del número de corridas (Por defecto: %(default)s)')
    parser.add_argument('-n', '--seleccion', default='red', help="Selección: un número, \"rojo\", \"negro\", \"par\", \"impar\", \"docena1\", \"docena2\", \"docena3\", \"col1\", \"col2\", \"col3\" (Por defecto: %(default)s)")
    parser.add_argument('-s', '--estrategia', default='m', choices=['m','d','f','p'], help="Estrategia a utilizar: \"m\" - Martingala, \"d\" - D'Alemnert, \"f\" - Fibonacci, \"p\" - Paroli (Por defecto: %(default)s)", )
    parser.add_argument('-a', '--capital', default=30000, help="Capital: \"i\" para infinito o el monto si es finito (Por defecto: %(default)s - Mínimo 1000)")
    # TODO type=tipoSeleccion y type=tipoCapital,

    args, unknown = parser.parse_known_args()
    number_of_batches = int(args.corridas)
    number_of_spins = int(args.tiradas)
    chosen_bet = args.seleccion
    chosen_strat = args.estrategia
    initial_capital = args.capital # TODO validar
    
    #print(f"Ejecutando {str(number_of_batches)} corridas de {str(number_of_spins)} tiradas para el número {str(chosen_number)}.")


def main():
    get_simulation_args()
    
    min_bet = 2500
    max_bet = 50000
    if (initial_capital == 'i'):
        max_bet = float('inf')

    roulette = Roulette(min_bet, max_bet)
    player = Player(initial_capital)

    match(chosen_strat):
        case 'm': strat = MartingalaStrat(roulette)
        case 'd': strat = DAlembertStrat(roulette)
        case 'o': strat = ParoliStrat(roulette)
        case 'f': strat = FibbonaciStrat(roulette)

    current_capital = 0
    bet = min_bet

    for _ in range(number_of_spins):
        number, player_won = roulette.spin(chosen_bet)
        variation = bet if player_won else -bet
        
        current_capital = player.update_capital(variation)

        if current_capital < min_bet:
            break

        bet = strat.CalcleNextBet(player_won, bet)


# Arranca el Programa
if __name__ == "__main__":
    main()
