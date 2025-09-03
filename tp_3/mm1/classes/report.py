from mm1.classes.theoretical_metrics import TheoreticalMetrics
from mm1.classes.graphics import Graphics
class MM1Report:
    def __init__(
        self,
        max_queue,
        arrival_rate,
        service_rate,
        avg_customer_in_system,
        avg_customer_in_queue,
        avg_time_in_system,
        avg_time_in_queue,
        server_usage,
        queue_length_probabilities,
        denial_probability,
    ):  
        self.max_queue = max_queue
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.avg_customer_in_system = avg_customer_in_system
        self.avg_customer_in_queue = avg_customer_in_queue
        self.avg_time_in_system = avg_time_in_system
        self.avg_time_in_queue = avg_time_in_queue
        self.server_usage = server_usage
        self.queue_length_probabilities = queue_length_probabilities
        self.denial_probability = denial_probability

    def print_summary(self):
        theoretical_metrics = TheoreticalMetrics(
            self.arrival_rate, self.service_rate, self.max_queue
        )
         
        print("\n\n--- Reporte promedio ---")
        print(f"Longitud máxima de la cola: {self.max_queue}")
        print(f"Tasa de arribo de clientes: {self.arrival_rate:.2f}")
        print(f"Tasa de servicio: {self.service_rate:.2f}\n")
        print(f"- Clientes promedio en el sistema:     {self.avg_customer_in_system:8.3f}                    |  Valor Teórico: {theoretical_metrics.avg_customers_in_system:8.3f}")
        print(f"- Clientes promedio en cola:           {self.avg_customer_in_queue:8.3f}                    |  Valor Teórico: {theoretical_metrics.avg_customers_in_queue:8.3f}")
        print(f"- Tiempo promedio en el sistema:       {self.avg_time_in_system:8.3f}                    |  Valor Teórico: {theoretical_metrics.avg_time_in_system:8.3f}")
        print(f"- Tiempo promedio en cola:             {self.avg_time_in_queue:8.3f}                    |  Valor Teórico: {theoretical_metrics.avg_time_in_queue:8.3f}")
        print(f"- Utilización del servidor:            {self.server_usage:8.3%}                    |  Valor Teórico: {theoretical_metrics.server_usage:8.3%}")
        print(f"- Probabilidad de denegación:          {self.denial_probability:8.3%}                    |  Valor Teórico: {theoretical_metrics.denial_probability:8.3%}")
        Graphics.generate_probabilities_chart(self.queue_length_probabilities, f"{self.max_queue}-{self.arrival_rate}-{self.service_rate}")


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

        
        avg_denial_probability =  sum(r.denial_probability for r in reports) / n

        return MM1Report(
            max_queue = reports[0].max_queue,
            arrival_rate = reports[0].arrival_rate,
            service_rate = reports[0].service_rate,
            avg_customer_in_system   = avg_L,
            avg_customer_in_queue    = avg_Lq,
            avg_time_in_system       = avg_W,
            avg_time_in_queue        = avg_Wq,
            server_usage             = avg_U,
            queue_length_probabilities = avg_probs,
            denial_probability=avg_denial_probability
        )
        