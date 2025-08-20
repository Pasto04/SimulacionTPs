class TheoreticalMetrics:
    def __init__(self, arrival_rate: float, service_rate: float, max_queue: int = float('inf')):
        self.lambda_rate = arrival_rate
        self.mu = service_rate
        self.K = max_queue
        self.rho = arrival_rate / service_rate if service_rate > 0 else float('inf')

        if self.K == float('inf'):
            self.infinite_queue()
        else:
            self.nfinite_queue()

    def infinite_queue(self):
        self.denial_probability = 0.0
        if self.rho >= 1:
            self.server_usage = 1.0
            self.avg_customers_in_system = float('inf')
            self.avg_customers_in_queue = float('inf')
            self.avg_time_in_system = float('inf')
            self.avg_time_in_queue = float('inf')
        else:
            self.server_usage = self.rho
            self.avg_customers_in_system = self.rho / (1 - self.rho)
            self.avg_customers_in_queue = self.rho**2 / (1 - self.rho)
            self.avg_time_in_system = 1 / (self.mu - self.lambda_rate)
            self.avg_time_in_queue = self.lambda_rate / (self.mu * (self.mu - self.lambda_rate))

    def nfinite_queue(self):

        K = self.K
        rho = self.rho

        if rho == 1:
            p0 = 1 / (K + 1)
        else:
            p0 = (1 - rho) / (1 - rho**(K + 1))

        p = [p0 * rho**n for n in range(K + 1)]

        effective_arrival_rate = self.lambda_rate * (1 - p[K])

        avg_customers_in_system = sum(n * p[n] for n in range(K + 1))

        avg_customers_in_queue = sum((n - 1) * p[n] for n in range(1, K + 1))

        avg_time_in_system = avg_customers_in_system / effective_arrival_rate if effective_arrival_rate > 0 else float('inf')
        avg_time_in_queue = avg_customers_in_queue / effective_arrival_rate if effective_arrival_rate > 0 else float('inf')


        self.server_usage = min(rho * (1 - p[K]), 1.0)
        self.avg_customers_in_system = avg_customers_in_system
        self.avg_customers_in_queue = avg_customers_in_queue
        self.avg_time_in_system = avg_time_in_system
        self.avg_time_in_queue = avg_time_in_queue
        self.denial_probability = p[K]
        self.effective_arrival_rate = effective_arrival_rate

