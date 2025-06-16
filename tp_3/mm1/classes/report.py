class MM1Report:
    def __init__(
        self,
        average_customer_in_system,
        average_customer_in_queue,
        average_time_in_system,
        average_time_in_queue,
        server_usage,
        queue_length_probabilities,
    ):
        self.average_customer_in_system = average_customer_in_system
        self.average_customer_in_queue = average_customer_in_queue
        self.average_time_in_system = average_time_in_system
        self.average_time_in_queue = average_time_in_queue
        self.server_usage = server_usage
        self.queue_length_probabilities = queue_length_probabilities

    def print_summary(self):
        print("\n--- Métricas de Rendimiento de la Simulación de Cola MM1 ---")
        print(f"- Clientes promedio en el sistema:     {self.average_customer_in_system:.3f}")
        print(f"- Clientes promedio en cola:           {self.average_customer_in_queue:.3f}")
        print(f"- Tiempo promedio en el sistema:       {self.average_time_in_system:.3f} unidades de tiempo")
        print(f"- Tiempo promedio en cola:             {self.average_time_in_queue:.3f} unidades de tiempo")
        print(f"- Utilización del servidor:            {self.server_usage:.3%}")
