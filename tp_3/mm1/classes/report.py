from mm1.classes.theoretical_metrics import TheoreticalMetrics
class MM1Report:
    def __init__(
        self,
        arrival_rate,
        service_rate,
        avg_customer_in_system,
        avg_customer_in_queue,
        avg_time_in_system,
        avg_time_in_queue,
        server_usage,
        queue_length_probabilities,
        denial_probability_by_queue_size,
    ):  
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.avg_customer_in_system = avg_customer_in_system
        self.avg_customer_in_queue = avg_customer_in_queue
        self.avg_time_in_system = avg_time_in_system
        self.avg_time_in_queue = avg_time_in_queue
        self.server_usage = server_usage
        self.queue_length_probabilities = queue_length_probabilities
        self.denial_probability_by_queue_size = denial_probability_by_queue_size

    def print_summary(self):
        theoretical_metrics = TheoreticalMetrics(
            self.arrival_rate, self.service_rate
        )
        print(f"- Clientes promedio en el sistema:     {self.avg_customer_in_system:8.3f}                    |  Valor Teórico: {theoretical_metrics.avg_customers_in_system:8.3f}")
        print(f"- Clientes promedio en cola:           {self.avg_customer_in_queue:8.3f}                    |  Valor Teórico: {theoretical_metrics.avg_customers_in_queue:8.3f}")
        print(f"- Tiempo promedio en el sistema:       {self.avg_time_in_system:8.3f} unidades de tiempo |  Valor Teórico: {theoretical_metrics.avg_time_in_system:8.3f}")
        print(f"- Tiempo promedio en cola:             {self.avg_time_in_queue:8.3f} unidades de tiempo |  Valor Teórico: {theoretical_metrics.avg_time_in_queue:8.3f}")
        print(f"- Utilización del servidor:            {self.server_usage:8.3%}                    |  Valor Teórico: {theoretical_metrics.server_usage:8.3%}")


    @staticmethod
    def aggregate_reports(reports: list['MM1Report']) -> 'MM1Report':
        n = len(reports)
        avg_L    = sum(report.avg_customer_in_system for report in reports) / n
        avg_Lq   = sum(report.avg_customer_in_queue for report in reports) / n
        avg_W    = sum(report.avg_time_in_system for report in reports) / n
        avg_Wq   = sum(report.avg_time_in_queue for report in reports) / n
        avg_U    = sum(report.server_usage for report in reports) / n

        max_level = max(
            max(r.queue_length_probabilities.keys()) 
            for r in reports
        )

        avg_probs = {
            k: sum(r.queue_length_probabilities.get(k, 0) for r in reports) / n
            for k in range(max_level + 1)
        }

        keys = reports[0].denial_probability_by_queue_size.keys()
        avg_denial_probability = {
            k: sum(r.denial_probability_by_queue_size[k] for r in reports) / n
            for k in keys
        }
        return MM1Report(
            arrival_rate = reports[0].arrival_rate,
            service_rate = reports[0].service_rate,
            avg_customer_in_system   = avg_L,
            avg_customer_in_queue    = avg_Lq,
            avg_time_in_system       = avg_W,
            avg_time_in_queue        = avg_Wq,
            server_usage             = avg_U,
            queue_length_probabilities = avg_probs,
            denial_probability_by_queue_size=avg_denial_probability
        )
        