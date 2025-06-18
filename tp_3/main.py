from inventory_model.classes.report import InventoryModelReport
from inventory_model.inventory_model_simulation import InventoryModelSimulation
from mm1.classes.report import MM1Report
from mm1.mm1_simulation import MM1Simulation
from numpy.random import default_rng
import argparse
import os

os.makedirs("images", exist_ok=True)

def get_simulation_args():
    parser = argparse.ArgumentParser(description="Simulador de Colas MM1 y Modelo de Inventario")

    # Parámetros MM1
    parser.add_argument("-a", "--mm1_arrival_rate", type=float, default=-1,
                        help="Tasa de arribos de los clientes (λ - clientes por hora) en el modelo de cola M/M/1 [default: %(default)s]")

    parser.add_argument("-s", "--service_rate", type=float, default=-1,
                        help="Tasa de servicio del servidor (μ - clientes por hora) en el modelo de cola M/M/1 [default: %(default)s]")

    # Parámetros Inventory Model
    parser.add_argument("-l", "--inv_model_arrival_rate", type=float, default=10,
                        help="Tasa de llegada de clientes (λ - clientes por mes) en el modelo de inventario [default: %(default)s]")

    parser.add_argument("-n", "--reorder_point", type=int, default=-1,
                        help="Punto de pedido (s) para el modelo de inventario [default: %(default)s]")

    parser.add_argument("-x", "--max_inventory_level", type=int, default=-1,
                        help="Nivel máximo de inventario (S) para el modelo de inventario [default: %(default)s]")

    parser.add_argument("-u", "--unit_cost", type=float, default=15000.0,
                        help="Costo por unidad [default: %(default)s]")

    parser.add_argument("-f", "--fixed_cost", type=float, default=3000.0,
                        help="Costo fijo por orden [default: %(default)s]")

    parser.add_argument("-m", "--holding_cost", type=float, default=750.0,
                        help="Costo de mantenimiento por unidad y por unidad de tiempo [default: %(default)s]")

    parser.add_argument("-b", "--backorder_cost", type=float, default=12000.0,
                        help="Costo de faltante por unidad y por unidad de tiempo [default: %(default)s]")

    parser.add_argument("-e", "--evaluation_period", type=float, default=1.0,
                        help="Período de evaluación del inventario [default: %(default)s]")

    parser.add_argument("-t", "--sim_time", type=float, default=120.0,
                        help="Tiempo total de simulación en meses [default: %(default)s]")

    args = parser.parse_args()
    print("Parámetros cargados para la simulación:")
    print(vars(args)) 
    return args

def main(): 
    sim_args = get_simulation_args()
    master_rng = default_rng(1234)
    runs_per_experiment = 10

    # MM1
    personalized_rates = sim_args.mm1_arrival_rate != -1 and sim_args.service_rate != -1
    service_rate = sim_args.service_rate if  personalized_rates else 1
    arrival_rates = [sim_args.mm1_arrival_rate] if personalized_rates else [0.25, 0.5, 0.75, 1.0, 1.25]
    queue_lengths = [0, 2, 5, 10, 50]

    avg_reports_by_queue_length: dict[float, dict[float, MM1Report]] = {}

    for queue_length in queue_lengths:
        avg_reports_by_rate_factor: dict[float, MM1Report] = {}
        for arrival_rate in arrival_rates:
            reports = []
            for _ in range(runs_per_experiment):
                sim_seed = master_rng.integers(0, 1_000_000_000)
                randomized = default_rng(sim_seed)
                simulation = MM1Simulation(arrival_rate, service_rate, random=randomized, max_queue=queue_length)
                report = simulation.run_simulation()
                reports.append(report)
            avg_reports_by_rate_factor[arrival_rate] = MM1Report.aggregate_reports(reports)
        avg_reports_by_queue_length[queue_length] = avg_reports_by_rate_factor


    print("\n== Métricas de Rendimiento de la Simulación de Cola MM1 ==")

    for queue_length, avg_reports_by_rate_factor in avg_reports_by_queue_length.items():
        for rate_factor, report in avg_reports_by_rate_factor.items():
            report.print_summary()


    # Inventory Model
    personalized_levels = sim_args.reorder_point != -1 and sim_args.max_inventory_level != -1

    reorder_points = [sim_args.reorder_point] if personalized_levels else [10, 15, 20, 25]
    max_inventory_levels = [sim_args.max_inventory_level] if personalized_levels else [20, 30, 60, 90]


    avg_reports: list[InventoryModelReport] = []
    for x in range (len(reorder_points)):
        reports = []
        for _ in range(runs_per_experiment):
            sim_seed = master_rng.integers(0, 1_000_000_000)
            randomized = default_rng(sim_seed)
            inventory_model = InventoryModelSimulation(sim_args.inv_model_arrival_rate, reorder_points[x], max_inventory_levels[x], sim_args.unit_cost, sim_args.fixed_cost, sim_args.holding_cost, sim_args.backorder_cost,inventory_evaluation_period=sim_args.evaluation_period, sim_time=sim_args.sim_time, random=randomized)
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
