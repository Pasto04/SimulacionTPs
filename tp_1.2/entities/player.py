
class Player:
    def __init__(self, capital:int):
        self.capital = [].append(capital)
        self.bets = []


    def update_capital(self, amount : int):
        self.capital.append(self.capital[-1] + amount)
        if self.capital[-1] == 0 or amount == 0:
            return 'Bankrupt!'
        return self.capital[-1]
    
    def get_current_capital(self):
        return self.capital[-1]
    
