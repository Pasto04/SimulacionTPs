class TheoreticalMetrics:
    def __init__(self,arrival_rate, service_rate):
        self.server_utilization = arrival_rate / service_rate

        self.avg_customers_in_system = self.server_utilization / (1 - self.server_utilization)

        self.avg_customers_in_queue = self.server_utilization**2 / (1 - self.server_utilization)

        self.avg_time_in_system = 1 / (service_rate - arrival_rate)

        self.avg_time_in_queue = (
            arrival_rate / (service_rate * (service_rate - arrival_rate))
        )
