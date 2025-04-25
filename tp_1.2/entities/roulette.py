import random
from typing import Union, Tuple, ClassVar, Set

class Roulette:
    RED: ClassVar[Set[int]]   = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    BLACK: ClassVar[Set[int]] = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    GROUP_BETS: ClassVar[Set[str]] = {
        'red','black','even','odd',
        'dozen1','dozen2','dozen3',
        'column1','column2','column3'
    }
    instance = None

    def __init__(self, min_bet: int, max_bet: int) -> None:
        self.min_bet = min_bet
        self.max_bet = max_bet

    @classmethod
    def get_instance(cls, min_bet=2500, max_bet=50000):
        if cls.instance is None:
            cls.instance = cls(min_bet, max_bet)
        return cls.instance
    
    @classmethod
    def validate_selection(cls, selection: Union[int, str]) -> Union[int, str]:
        """
        Validate and normalize a bet selection.  
        Returns:
          - an int 0-36 for a straight-up number bet  
          - one of the lowercased group-bet strings  
        Raises ValueError if invalid.
        """
        if isinstance(selection, int):
            if 0 <= selection <= 36:
                return selection
            raise ValueError(f"Number bet must be 0-36, got {selection}")
        
        sel = selection.lower()
        if sel in cls.GROUP_BETS:
            return sel
        raise ValueError(f"Invalid group bet: {selection!r}")

    def spin(self, selected_bet: Union[int, str], bet: int) -> Tuple[bool, int]:
        """
        Spins the wheel (0-36) and returns (number, did_win).
        Assumes selected_bet has already passed through validate_selection().
        """
        number = random.randint(0, 36)

        if isinstance(selected_bet, int):
            win = selected_bet == number
            capital_variation = bet*35 if win else -bet
            return win, capital_variation

        # Group bets (0 auto-loses)
        if number == 0:
            return False, -bet

        if selected_bet == 'red':
            win = number in self.RED
            capital_variation = bet if win else -bet
        elif selected_bet == 'black':
            win = number in self.BLACK
            capital_variation = bet if win else -bet
        elif selected_bet == 'even':
            win = (number % 2 == 0)
            capital_variation = bet if win else -bet
        elif selected_bet == 'odd':
            win = (number % 2 == 1)
            capital_variation = bet if win else -bet
        elif selected_bet == 'dozen1':
            win = 1 <= number <= 12
            capital_variation = 2*bet if win else -bet
        elif selected_bet == 'dozen2':
            win = 13 <= number <= 24
            capital_variation = 2*bet if win else -bet
        elif selected_bet == 'dozen3':
            win = 25 <= number <= 36
            capital_variation = 2*bet if win else -bet
        elif selected_bet == 'column1':
            win = (number % 3 == 1)
            capital_variation = 2*bet if win else -bet
        elif selected_bet == 'column2':
            win = (number % 3 == 2)
            capital_variation = 2*bet if win else -bet
        else:  # 'column3'
            win = (number % 3 == 0)
            capital_variation = 2*bet if win else -bet

        return win, capital_variation

