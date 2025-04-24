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


import argparse
import random
from entities.strats import FibbonaciStrat, MartingalaStrat, DAlembertStrat, ParoliStrat
from entities.player import Player
from entities.roulette import Roulette
from entities.graphics import GenerateGraphics

chosen_bet = number_of_spins = number_of_batches = initial_capital = 0
chosen_strat = ''

#TODO: Listas de colores y grupos de apuestas, estan aca por se necesitan en el tipo de apuestas, considerar mover a otro lado, pero por ahora es funcional.

RED   = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
GROUP_BETS = { 
    'red', 'black', 'even', 'odd',
    'dozen1', 'dozen2', 'dozen3',
    'column1', 'column2', 'column3'
}

def valid_bet(value: str):
    if value.isdigit():
        ivalue = int(value)
        if 0 <= ivalue <= 36:
            return ivalue
        raise argparse.ArgumentTypeError(f"Número fuera de rango: {ivalue} (permitido: 0–36)")

    value_lower = value.lower()
    if value_lower in GROUP_BETS:
        return value_lower

    raise argparse.ArgumentTypeError(
        f"'{value}' no es una apuesta válida. Usa un número del 0 al 36 o uno de: {', '.join(GROUP_BETS)}"
    )

def valid_capital(value: str):
    if value.lower() == 'i':
        return 'i' #esto chequea si pusiste que sea infinto

    try:
        amount = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' no es un número válido ni 'i' para infinito.")
    
    if amount < 2500:
        raise argparse.ArgumentTypeError(f"Capital mínimo es 2500. Ingresaste: {amount}")
    
    return amount # aca te devuelve lo que ingresaste, sino no cumple no llega hasta aca


def get_simulation_args():
    global chosen_bet, number_of_spins, number_of_batches, chosen_strat, initial_capital
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tiradas",  default=100, help="Valor del número de tiradas por corrida (100 por defecto)")
    parser.add_argument('-c', '--corridas', default=15, type=int, help='Valor del número de corridas (Por defecto: %(default)s)')
    parser.add_argument("-n", "--seleccion", default="red", type=valid_bet, help="Selección: un número, \"red\", \"black\", \"even\", \"odd\", \"dozen1\", \"dozen2\", \"dozen3\", \"column1\", \"column2\", \"column3\" (Por defecto: %(default)s)")
    parser.add_argument('-s', '--estrategia', default='m', choices=['m','d','f','o'], help="Estrategia a utilizar: \"m\" - Martingala, \"d\" - D'Alemnert, \"f\" - Fibonacci, \"o\" - Paroli (Por defecto: %(default)s)", )
    parser.add_argument('-a', '--capital', default=50000, type=valid_capital, help="Capital: \"i\" para infinito o el monto si es finito (Por defecto: %(default)s - Mínimo 2500)")

    args, unknown = parser.parse_known_args()
    number_of_batches = int(args.corridas)
    number_of_spins = int(args.tiradas)
    chosen_bet = args.seleccion
    chosen_strat = args.estrategia
    initial_capital = args.capital 
    
    print(f"Ejecutando simulación.")


def generate_one_batch_graphics(players: list[Player], min_bet: int):
    batch_show_number = random.randint(1, number_of_batches)
    selected_player = players[batch_show_number-1]
    
    #aca calculo cual deberia ser el valor esperado segun apuesta
    match(chosen_bet):
            case int() as number if 0 <= number <= 36:
                expected_value_based_on_bet = ( 1 / 37 ) #The chance of winning a straight-up bet is 1 in 37 (0-36)
            case "red" | "black":
                expected_value_based_on_bet = ( 18 / 36 ) #The chance of winning a color bet is 18 in 36 (0 auto-loses)
            case "even" | "odd":
                expected_value_based_on_bet = ( 18 / 36 ) #The chance of winning an even/odd bet is 18 in 36 (0 auto-loses)
            case "dozen1" | "dozen2" | "dozen3":
                expected_value_based_on_bet = ( 12 / 36 ) #The chance of winning a dozen bet is 12 in 36 (0 auto-loses)
            case "column1" | "column2" | "column3":
                expected_value_based_on_bet = ( 12 / 36 ) #The chance of winning a column bet is 12 in 36 (0 auto-loses)
            case _:
                raise ValueError(f"Apuesta desconocida: {chosen_bet}")

    GenerateGraphics.generate_bar_chart("Frecuencia relativa de victorias", 1, "Número de tirada", "Frecuencia relativa", selected_player.get_relative_freq_spins_won(), expected_value_based_on_bet)
    GenerateGraphics.generate_line_chart("Flujo de caja", 2, "Número de tirada", "Cantidad de capital", selected_player.get_capital(), initial_capital)
    GenerateGraphics.generate_bar_chart_from_counter("Frecuencia del monto de las apuestas", 3, "Monto de apuesta", "Frecuencia absoluta", selected_player.get_bets(), min_bet)
    
    title = f"CORRIDA NÚMERO {batch_show_number}\n"
    title += f"Selección: {chosen_bet} - Estrategia: {selected_player.get_strat().get_name()} - Capital inicial: {initial_capital}"
    GenerateGraphics.show_graphics(title)


def generate_general_graphics(players: list[Player]):
    capitals_array = []
    spins_count = []

    for p in players:
        capitals_array.append(p.get_capital())
        spins_count.append(len(p.get_bets()))

    #aca calculo cual deberia ser el valor esperado segun apuesta
    match(chosen_bet):
        case int() as number if 0 <= number <= 36:
            expected_value_based_on_bet = ( 1 / 37 ) #The chance of winning a straight-up bet is 1 in 37 (0-36)
        case "red" | "black":
            expected_value_based_on_bet = ( 18 / 36 ) #The chance of winning a color bet is 18 in 36 (0 auto-loses)
        case "even" | "odd":
            expected_value_based_on_bet = ( 18 / 36 ) #The chance of winning an even/odd bet is 18 in 36 (0 auto-loses)
        case "dozen1" | "dozen2" | "dozen3":
            expected_value_based_on_bet = ( 12 / 36 ) #The chance of winning a dozen bet is 12 in 36 (0 auto-loses)
        case "column1" | "column2" | "column3":
            expected_value_based_on_bet = ( 12 / 36 ) #The chance of winning a column bet is 12 in 36 (0 auto-loses)
        case _:
            raise ValueError(f"Apuesta desconocida: {chosen_bet}")

    GenerateGraphics.generate_bar_chart("Cantidad de tiradas por jugador", 1, "Número de jugador", "Cantidad de tiradas", spins_count, expected_value_based_on_bet)
    GenerateGraphics.generate_line_chart("Flujo de caja", 2, "Número de tirada", "Cantidad de capital", capitals_array, initial_capital, True)

    title = f"MÚLTIPLES CORRIDAS\n"
    title += f"Corridas: {number_of_batches} - Selección: {chosen_bet} - Estrategia: {players[0].get_strat().get_name()} - Capital inicial: {initial_capital}"
    GenerateGraphics.show_graphics(title)


def main():
    get_simulation_args()
    
    min_bet = 2500
    max_bet = 50000
    if (initial_capital == 'i'):
        max_bet = float('inf')

    roulette = Roulette(min_bet, max_bet)
    players: list[Player] = []

    for _ in range(number_of_batches):
        bet = min_bet
        player = Player(initial_capital)

        match(chosen_strat):
            case 'm': strat = MartingalaStrat(roulette, player)
            case 'd': strat = DAlembertStrat(roulette, player)
            case 'o': strat = ParoliStrat(roulette, player)
            case 'f': strat = FibbonaciStrat(roulette, player)

        player.set_strat(strat)
        players.append(player)

        for _ in range(number_of_spins):
            player.add_new_bet(bet)
            player_won, capital_variation = roulette.spin(chosen_bet, bet)

            current_capital = player.update_capital(capital_variation)

            if current_capital < min_bet:
                break

            bet = strat.CalcleNextBet(player_won, bet)


    #TODO depende a lo que juege el expected value (apuesta a qúe)
    generate_one_batch_graphics(players, min_bet)
    generate_general_graphics(players)


# arranca el programa 
if __name__ == "__main__":
    main()

