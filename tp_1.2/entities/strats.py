from abc import ABC, abstractmethod
from typing import List, Optional
from entities.roulette import Roulette


class Strat(ABC):
    def __init__(self, roulette: Roulette, name = 'defaultName', description = 'defaultDescription'):
        self.name =  name
        self.description = description
        self.min_bet = roulette.min_bet
        self.max_bet = roulette.max_bet

    def __str__(self):
        return f"Strat(name={self.name}, description={self.description}, min_bet={self.min_bet}, max_bet={self.max_bet})"
    
    @abstractmethod
    def CalcleNextBet (self, player_won: bool, bet: int):
        pass

    def ControlNextBet(self, desired_bet) -> int:
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
    '''
    
    def __init__(self, roulette: Roulette) -> None:
        super().__init__('Fibbonaci', 'Fibbonaci betting strategy', roulette.min_bet, roulette.max_bet)
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
    '''

    def __init__(self, roulette: Roulette) -> None:
        super().__init__(roulette, 'Martingala', 'Martingala betting strategy')
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
    
      TODO: check if two validations are needed??
    '''

    def __init__(self, roulette: Roulette) -> None:
        super().__init__(roulette, "D'Alembert", "D'Alembert betting strategy")
        self.current_bet: int = roulette.min_bet

    def CalcleNextBet(self, player_won: bool, bet: int) -> int:
        if player_won:
            self.current_bet = max(self.current_bet - self.min_bet, self.min_bet)
        else:
            self.current_bet = min(self.current_bet + self.min_bet, self.max_bet)

        return super.ControlNextBet(self.current_bet)

class ParoliStrat (Strat):
    '''
    Implements the classic Paroli (reverse-Martingale) roulette progression:
    - on a win, double your previous bet (up to a cap)
    - on a loss, reset back to the base bet
    '''
    
    def __init__(self, roulette: Roulette, max_doubles: Optional[int] = 3) -> None:
        super().__init__(roulette, 'Paroli', 'Paroli betting strategy')
        self.win_streak: int = 0
        self.max_doubles: Optional[int] = max_doubles

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

