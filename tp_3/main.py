from mm1.mm1_simulation import MM1Simulation
from inventory_model.inventory_model_simulation import InventoryModelSimulation
from numpy.random import default_rng
from mm1.classes.report import MM1Report

def main():
    master_rng = default_rng(1234)
    runs_per_experiment = 10
    service_rate = 1
    arrival_rate_factors = [0.25, 0.5, 0.75, 1.0, 1.25]

    avg_reports_by_rate_factor = {}
    for factor in arrival_rate_factors:
        arrival_rate = service_rate * factor
        print(f"\n== Simulando para arrival_rate = {arrival_rate:.2f} y service_rate = {service_rate:.2f} ==")
        reports = []

        for run in range(runs_per_experiment):
            sim_seed = master_rng.integers(0, 1_000_000_000)
            randomized = default_rng(sim_seed)
            simulation = MM1Simulation(arrival_rate, service_rate,  random=randomized)
            report = simulation.run_simulation()
            reports.append(report)
        avg_reports_by_rate_factor[factor] = MM1Report.aggregate_reports(reports)
        
    for factor, report in avg_reports_by_rate_factor.items():
        print(f"\n== Reporte promedio para arrival_rate = {report.arrival_rate:.2f} y service_rate = {report.service_rate:.2f} ==")
        report.print_summary()
    inventory_model = InventoryModelSimulation(2, 15000, 3000, 800, 5000)
    inventory_model.run_simulation()


if __name__ == "__main__":
    main()