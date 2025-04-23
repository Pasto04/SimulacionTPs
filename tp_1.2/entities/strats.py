from typing import List, Optional

class Strat():
    def __init__(self, name = 'deafultName', descrption = 'defaultDescription', min_bet = 0, max_bet = float('inf'), available_money = float('inf')):
        self.name =  name
        self.description = descrption
        self.min_bet = min_bet
        self.max_bet = max_bet

    def __str__(self):
        return f"Strat(name={self.name}, description={self.description}, min_bet={self.min_bet}, max_bet={self.max_bet})"
    
    def ChooseNextBet (self, last_bet, last_result):
        pass

    def ControlNextBet(self, desired_bet) -> int:
        """
        Determine the next wager amount, with these rules:
        1) If you dont have enough to meet the minimum, you cant bet (return 0).
        2) Otherwise, never go below self.min_bet.
        3) Never exceed your available money or your strategys max_bet.
        """
        # 1) Not enough for the minimum? No bet.
        if self.available_money < self.min_bet:
            return 0

        # 2) Compute your true upper‐limit:
        #    if max_bet is infinite, cap is your bankroll; else it's min(max_bet, bankroll)
        if self.max_bet == float('inf'):
            effective_max = self.available_money
        else:
            effective_max = min(self.max_bet, self.available_money)

        # 3) Clamp desired_bet into the range [min_bet, effective_max]
        wager = max(desired_bet, self.min_bet)
        wager = min(wager, effective_max)
        return wager


class FibbonaciStrat():

    #Implements the classic Fibonacci betting progression:
    #  – on a loss, step forward in the sequence
    #  – on a win, step back two places (but never below the first)
    #Bet size = sequence[current_index] * min_bet

    def __init__(self, min_bet: int, max_bet: int) -> None:
        super().__init__('Fibbonaci', 'Fibbonaci betting strategy', min_bet, max_bet)
        self.sequence: List[int] = [1, 1]   # fib[0]=1, fib[1]=1
        self.current_index: int  = 0         # points into self.sequence

    def ChooseNextBet(self, win: bool) -> int:
        # advance or retreat in the fib sequence
        if win:
            # on a win, go back two steps
            self.current_index = max(self.current_index - 2, 0)
        else:
            # on a loss, step forward
            self.current_index += 1

        # ensure the sequence list is long enough
        while self.current_index >= len(self.sequence):
            self.sequence.append(self.sequence[-1] + self.sequence[-2])

        return super.ControlNextBet(self.sequence[self.current_index] * self.min_bet)


class MartingalaStrat ():

    #Implements the classic Martingale roulette progression:
    #  – on a loss, double your previous bet
    #  – on a win, reset back to the base bet

    def __init__(self, min_bet: int, max_bet: int) -> None:
        # name, description, min & max come from your Strat base
        super().__init__('Martingala', 'Martingala betting strategy', min_bet, max_bet)
        self.loss_streak: int = 0

    def ChooseNextBet(self, win: bool) -> int:
        if win:
            # reset after any win
            self.loss_streak = 0
        else:
            # increment on each loss
            self.loss_streak += 1

        # each loss doubles the base
        next_bet = self.min_bet * (2 ** self.loss_streak)
        return super.ControlNextBet(next_bet)

class DAlembertStrat ():

    #Implements the classic D’Alembert roulette progression:
    #  – on a loss, increase your bet by one unit (min_bet)
    #  – on a win, decrease your bet by one unit, but never below min_bet
    #
    #  TODO: check if two validations are needed??

    def __init__(self, min_bet: int, max_bet: int) -> None:
        # set name/description/min/max via your base
        super().__init__("D'Alembert", "D'Alembert betting strategy", min_bet, max_bet)
        self.current_bet: int = min_bet

    def ChooseNextBet(self, win: bool) -> int:
        if win:
            # step back one unit on a win, floor at min_bet
            self.current_bet = max(self.current_bet - self.min_bet, self.min_bet)
        else:
            # step up one unit on a loss, cap at max_bet
            self.current_bet = min(self.current_bet + self.min_bet, self.max_bet)

        return super.ControlNextBet(self.current_bet)

class ParoliStrat ():
    
    #Implements the classic Paroli (reverse‐Martingale) roulette progression:
    #  – on a win, double your previous bet (up to a cap)
    #  – on a loss, reset back to the base bet
    

    def __init__(self, min_bet: int, max_bet: int, max_doubles: Optional[int] = 3) -> None:
        # initialize name/description/min/max via your Strat base
        super().__init__('Paroli', 'Paroli betting strategy', min_bet, max_bet)
        self.win_streak: int = 0
        self.max_doubles: Optional[int] = max_doubles

    def ChooseNextBet(self, win: bool) -> int:
        if win:
            # increment the number of consecutive wins
            self.win_streak += 1
            # if there's a cap on how many times you double, enforce it
            if self.max_doubles is not None:
                self.win_streak = min(self.win_streak, self.max_doubles)
            # each win doubles the base wager
            desired = self.min_bet * (2 ** self.win_streak)
        else:
            # any loss resets the streak
            self.win_streak = 0
            desired = self.min_bet

        # apply your table‐limit & strategy‐limit logic
        return super.ControlNextBet(desired)

