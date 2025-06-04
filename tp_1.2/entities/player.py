class Player:
    def __init__(self, capital: int):
        self.wons_count = 0
        self.capital = [capital]
        self.infinite_capital = capital == 0

        self.bets = []
        self.relative_freq_spins_won = []
        self.bet_step_stats = {}

    def update_capital(self, amount: int):
        self.capital.append(self.capital[-1] + amount)

        if amount > 0:
            self.wons_count += 1
        
        
        spins_count = len(self.relative_freq_spins_won) + 1
        self.relative_freq_spins_won.append(self.wons_count/spins_count)

        return self.capital[-1]

    def update_wins_by_step(self, win: bool, strat_step: int):
        if strat_step not in self.bet_step_stats:
            self.bet_step_stats[strat_step] = {"wins": 0, "bets": 0}

        self.bet_step_stats[strat_step]["bets"] += 1
        if win:
            self.bet_step_stats[strat_step]["wins"] += 1

    def get_win_rate_by_step(self):
        max_step = max(self.bet_step_stats.keys())
        rates = []

        for step in range(1, max_step + 1):
            stats = self.bet_step_stats.get(step, {"bets": 0, "wins": 0})
            bets = stats["bets"]
            wins = stats["wins"]
            rate = wins / bets if bets > 0 else 0.0
            rates.append(rate)

        return rates

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
    
    def get_infinite_capital(self):
        return self.infinite_capital

