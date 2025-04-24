class Player:
    def __init__(self, capital: int):
        self.capital = [capital]


    def update_capital(self, amount: int):
        self.capital.append(self.capital[-1] + amount)
        return self.capital[-1]


    def get_current_capital(self):
        return self.capital[-1]

