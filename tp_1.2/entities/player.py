class Player:
    def __init__(self, capital: int):
        self.wons_count = 0
        self.capital = [capital]
        self.bets = []
        self.relative_freq_spins_won = []


    def update_capital(self, amount: int):
        self.capital.append(self.capital[-1] + amount)
        if amount > 0:
            self.wons_count += 1
        
        spins_count = len(self.relative_freq_spins_won) + 1
        self.relative_freq_spins_won.append(self.wons_count/spins_count)

        return self.capital[-1]


    def get_current_capital(self):
        return self.capital[-1]

    def add_new_bet(self, new_bet: int):
        self.bets.append(new_bet)

    def get_capital(self):
        return self.capital

    def get_bets(self):
        return self.bets

    def get_relative_freq_spins_won(self):
        return self.relative_freq_spins_won

    def set_strat(self, strat):
        self.strat = strat

    def get_strat(self):
        return self.strat

