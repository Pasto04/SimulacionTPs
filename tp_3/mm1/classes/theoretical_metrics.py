class TheoreticalMetrics:
    def __init__(self,arrival_rate, service_rate):
        if arrival_rate >= service_rate:
            self.server_usage = 1
            self.avg_customers_in_system = float('inf')

            self.avg_customers_in_queue = float('inf')

            self.avg_time_in_system = float('inf')

            self.avg_time_in_queue = float('inf')
        else:
            self.server_usage = arrival_rate / service_rate

            self.avg_customers_in_system = self.server_usage / (1 - self.server_usage)

            self.avg_customers_in_queue = self.server_usage**2 / (1 - self.server_usage)

            self.avg_time_in_system = 1 / (service_rate - arrival_rate)

            self.avg_time_in_queue = (
                arrival_rate / (service_rate * (service_rate - arrival_rate))
            )

