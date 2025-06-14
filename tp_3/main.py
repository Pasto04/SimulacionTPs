from mm1.mm1_simulation import MM1Simulation


def main():
    arrival_factors = [0.25, 0.5, 0.75, 1.0, 1.25]
    runs_per_experiment = 10
    
    mm1_simulation = MM1Simulation(1.2,1.3)
    mm1_simulation.run_simulation()


if __name__ == "__main__":
    main()
