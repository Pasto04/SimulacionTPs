from inventory_model.classes.report import InventoryModelReport
from inventory_model.inventory_model_simulation import InventoryModelSimulation
from mm1.classes.report import MM1Report
from mm1.mm1_simulation import MM1Simulation
from numpy.random import default_rng

def main():
    master_rng = default_rng(1234)
    runs_per_experiment = 10
    
    # MM1 Model
    service_rate = 1
    arrival_rate_factors = [0.25, 0.5, 0.75, 1.0, 1.25]

    avg_reports_by_rate_factor: dict[float, MM1Report] = {}
    for factor in arrival_rate_factors:
        arrival_rate = service_rate * factor
        reports = []

        for _ in range(runs_per_experiment):
            sim_seed = master_rng.integers(0, 1_000_000_000)
            randomized = default_rng(sim_seed)
            simulation = MM1Simulation(arrival_rate, service_rate, random=randomized)
            report = simulation.run_simulation()
            reports.append(report)

        avg_reports_by_rate_factor[factor] = MM1Report.aggregate_reports(reports)

    print("\n== Métricas de Rendimiento de la Simulación de Cola MM1 ==")
    for factor, report in avg_reports_by_rate_factor.items():
        print("\n\n--- Reporte promedio ---")
        print(f"Tasa de arribo de clientes: {report.arrival_rate:.2f}")
        print(f"Tasa de servicio: {report.service_rate:.2f}\n")
        report.print_summary()


    # Inventory Model
    reorder_points = [15, 20, 25]
    max_inventory_levels = [30, 60, 90]

    avg_reports: list[InventoryModelReport] = []
    for x in range (len(reorder_points)):
        reports = []
        for _ in range(runs_per_experiment):
            sim_seed = master_rng.integers(0, 1_000_000_000)
            randomized = default_rng(sim_seed)
            inventory_model = InventoryModelSimulation(2, reorder_points[x], max_inventory_levels[x], 15000, 3000, 800, 5000)
            report = inventory_model.run_simulation()
            reports.append(report)

        avg_reports.append(InventoryModelReport.aggregate_reports(reports))
    
    print("\n\n== Métricas de Rendimiento del Modelo de Inventario ==")
    for report in avg_reports:
        print("\n\n--- Reporte promedio ---")
        print(f"Tasa de arribo de clientes: {report.customer_arrival_rate}")
        print(f"Punto de reposición: {report.reorder_point}")
        print(f"Capacidad máxima inventario: {report.max_inventory_level}\n")
        report.print_summary()



if __name__ == "__main__":
    main()
