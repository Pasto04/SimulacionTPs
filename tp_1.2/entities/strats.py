from abc import ABC, abstractmethod
from typing import List
from entities.roulette import Roulette
from entities.player import Player


class Strat(ABC):
    def __init__(self, roulette: Roulette, player: Player, name = 'defaultName', description = 'defaultDescription'):
        self.name =  name
        self.description = description
        self.min_bet = roulette.min_bet
        self.max_bet = roulette.max_bet
        self.player = player

    def __str__(self):
        return f"Strat(name={self.name}, description={self.description}, min_bet={self.min_bet}, max_bet={self.max_bet})"

    def get_name(self):
        return self.name

    @abstractmethod
    def CalcleNextBet (self, player_won: bool, bet: int):
        pass

    def ControlNextBet(self, desired_bet) -> int:
        if (self.player.get_infinite_capital()):
            if (desired_bet > self.max_bet):
                return self.max_bet
            return desired_bet

        if (self.player.get_current_capital() < desired_bet):
            desired_bet = self.player.get_current_capital()

        if (desired_bet > self.max_bet):
            return self.max_bet

        if (desired_bet < self.min_bet):
            return self.min_bet

        return desired_bet


class FibbonaciStrat(Strat):
    '''
    Implements the classic Fibonacci betting progression:
    - on a loss, step forward in the sequence
    - on a win, step back two places (but never below the first)
    #Bet size = sequence[current_index] * min_bet
    Source: http
    s://blog.sportium.es/3-simples-estrategias-para-ganar-en-la-ruleta-que-cualquiera-puede-intentar/
    '''
    
    def __init__(self, roulette: Roulette, player: Player) -> None:
        super().__init__(roulette, player, 'Fibbonaci', 'Fibbonaci betting strategy')
        self.sequence: List[int] = [1, 1]
        self.current_index: int  = 0

    def CalcleNextBet(self, player_won: bool, bet: int) -> int:
        if player_won:
            self.current_index = max(self.current_index - 2, 0)
        else:
            self.current_index += 1

        while self.current_index >= len(self.sequence):
            self.sequence.append(self.sequence[-1] + self.sequence[-2])

        return super().ControlNextBet(self.sequence[self.current_index] * self.min_bet)


class MartingalaStrat (Strat):
    '''
    Implements the classic Martingale roulette progression:
    - on a loss, double your previous bet
    - on a win, reset back to the base bet
    Source: https://blog.sportium.es/3-simples-estrategias-para-ganar-en-la-ruleta-que-cualquiera-puede-intentar/
    '''

    def __init__(self, roulette: Roulette, player: Player) -> None:
        super().__init__(roulette, player, 'Martingala', 'Martingala betting strategy')
        self.loss_streak: int = 0

    def CalcleNextBet(self, player_won: bool, bet: int) -> int:
        if player_won:
            self.loss_streak = 0
        else:
            self.loss_streak += 1

        next_bet = self.min_bet * (2 ** self.loss_streak)
        return super().ControlNextBet(next_bet)

class DAlembertStrat (Strat):
    '''
    Implements the classic D’Alembert roulette progression:
    - on a loss, increase your bet by one unit (min_bet)
    - on a win, decrease your bet by one unit, but never below min_bet
    Source: https://blog.sportium.es/3-simples-estrategias-para-ganar-en-la-ruleta-que-cualquiera-puede-intentar/
    '''

    def __init__(self, roulette: Roulette, player: Player) -> None:
        super().__init__(roulette, player, "D'Alembert", "D'Alembert betting strategy")
        self.current_bet: int = roulette.min_bet

    def CalcleNextBet(self, player_won: bool, bet: int) -> int:
        if player_won:
            self.current_bet = max(self.current_bet - self.min_bet, self.min_bet)
        else:
            self.current_bet = min(self.current_bet + self.min_bet, self.max_bet)

        return super().ControlNextBet(self.current_bet)

class ParoliStrat (Strat):
    '''
    Implements the classic Paroli (reverse-Martingale) roulette progression:
    - on a win, double your previous bet (up to a cap)
    - on a loss, reset back to the base bet
    Source: https://blog.sportium.es/3-simples-estrategias-para-ganar-en-la-ruleta-que-cualquiera-puede-intentar/
    '''
    
    def __init__(self, roulette: Roulette, player: Player) -> None:
        super().__init__(roulette, player, 'Paroli', 'Paroli betting strategy')
        self.win_streak: int = 0
        self.max_doubles = 3

    def CalcleNextBet(self, player_won: bool, bet: int) -> int:
        if player_won:
            self.win_streak += 1

            if self.max_doubles is not None:
                self.win_streak = min(self.win_streak, self.max_doubles)

            desired = self.min_bet * (2 ** self.win_streak)
        else:

            self.win_streak = 0
            desired = self.min_bet

        return super().ControlNextBet(desired)

