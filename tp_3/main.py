from mm1.mm1_simulation import MM1Simulation
from inventory_model.inventory_model_simulation import InventoryModelSimulation


def main():
    runs_per_experiment = 10
    service_rate = 1
    arrival_rate_factors = [0.25, 0.5, 0.75, 1.0, 1.25]

    for factor in arrival_rate_factors:
        arrival_rate = service_rate * factor
        print(f"\n== Simulando para arrival_rate = {arrival_rate:.2f} y service_rate = {service_rate:.2f} ==")
        reports = []

        for run in range(runs_per_experiment):
            simulation = MM1Simulation(arrival_rate, service_rate)
            report = simulation.run_simulation()
            reports.append(report)

        #TODO calcular promedio de las runs y mostrar el reporte final

    inventory_model = InventoryModelSimulation(2, 15000, 3000, 800, 5000)
    inventory_model.run_simulation()


if __name__ == "__main__":
    main()
