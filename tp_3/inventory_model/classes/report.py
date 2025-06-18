import matplotlib.pyplot as plt

class InventoryModelReport:
  
    def __init__(
        self,
        customer_arrival_rate: float,
        reorder_point: int,
        max_inventory_level: int,
        ordering_cost: float,
        holding_cost: float,
        backorder_cost: float,
        total_cost: float,
    ):
        self.customer_arrival_rate = customer_arrival_rate
        self.reorder_point = reorder_point
        self.max_inventory_level = max_inventory_level
        self.ordering_cost = ordering_cost
        self.holding_cost = holding_cost
        self.backorder_cost = backorder_cost
        self.total_cost = total_cost


    def print_summary(self):
        print(f"- Costo de orden:                      ${self.ordering_cost:12,.2f}")
        print(f"- Costo de mantenimiento:              ${self.holding_cost:12,.2f}")
        print(f"- Costo de faltante:                   ${self.backorder_cost:12,.2f}")
        print(f"- Costo total:                         ${self.total_cost:12,.2f}")
        self.plot_cost_pie_chart()

    @staticmethod
    def aggregate_reports(reports: list['InventoryModelReport']) -> 'InventoryModelReport':
        n = len(reports)
        avg_ordering_cost = sum(r.ordering_cost for r in reports) / n
        avg_holding_cost = sum(r.holding_cost for r in reports) / n
        avg_backorder_cost = sum(r.backorder_cost for r in reports) / n
        avg_total_cost = sum(r.total_cost for r in reports) / n

            
        return InventoryModelReport(
            reports[0].customer_arrival_rate,
            reports[0].reorder_point,
            reports[0].max_inventory_level,
            ordering_cost=avg_ordering_cost,
            holding_cost=avg_holding_cost,
            backorder_cost=avg_backorder_cost,
            total_cost=avg_total_cost
        )
        
    def plot_cost_pie_chart(self):
        labels = ['Pedido', 'Mantenimiento', 'Faltantes']
        costs = [self.ordering_cost, self.holding_cost, self.backorder_cost]

        plt.figure(figsize=(6, 6))
        plt.pie(costs, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Distribución porcentual de costos en la simulación")
        plt.axis('equal')  
        plt.show()
