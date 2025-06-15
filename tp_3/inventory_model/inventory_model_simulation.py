import numpy as np
from numpy.random import Generator, default_rng
from typing import Literal
from inventory_model.classes.statistical_counters import StatisticalCounters
from inventory_model.classes.system_state import SystemState


class InventoryModelSimulation:
    def __init__(self, customer_arrival_rate, inventory_evaluation_period=1, sim_time=120, random:Generator = default_rng()):
        self.customer_arrival_rate = customer_arrival_rate
        self.inventory_evaluation_period = inventory_evaluation_period
        self.sim_time = sim_time
        self.random = random


    def run_simulation(self):
        self.init_simulation()

        while self.clock < self.sim_time:
            event_type = self.advance_time()

            if event_type == "customer_arrival":
                self.handle_customer_arrival()
            elif event_type == "order_arrival":
                self.handle_order_arrival()
            else:
                self.evaluate_inventory()

        self.generate_report()


    def init_simulation(self):
        self.clock = 0
        self.generate_next_customer_arrival()
        self.next_order_arrival_time = np.inf
        self.next_inventory_evaluation_time = self.inventory_evaluation_period

        self.system_state = SystemState()
        self.statistical_counters = StatisticalCounters()


    def advance_time(self) -> Literal["customer_arrival", "order_arrival", "inventory_evaluation"]:
        event_times = {
            "customer_arrival": self.next_customer_arrival_time,
            "order_arrival": self.next_order_arrival_time,
            "inventory_evaluation": self.inventory_evaluation_time
        }

        next_event_type = min(event_times, key=event_times.get)
        self.clock = event_times[next_event_type]
        return next_event_type


    def handle_customer_arrival(self):
        #TODO update_areas() -> calcular i+ e i- en el momento adecuado
        demand = self.generate_customer_demand()
        self.system_state.inventory_level -= demand
        self.generate_next_customer_arrival()


    def handle_order_arrival(self):
        #TODO update_areas() -> calcular i+ e i- en el momento adecuado
        self.system_state.inventory_level += self.system_state.last_order_quantity
        self.system_state.last_order_quantity = 0
        self.next_order_arrival_time = np.inf


    def evaluate_inventory(self):
        if self.system_state.inventory_level < self.system_state.reorder_point:
            pass
            #determinar cantidad a pedir
            #Incur ordering cost and gather statistics
            #order arrival event para this order

        self.next_inventory_evaluation_time += self.inventory_evaluation_period


    def generate_next_customer_arrival(self):
        self.next_customer_arrival_time = self.clock + self.random.exponential(scale = 1/self.customer_arrival_rate)

    def generate_customer_demand(self):
        u = np.random.uniform()
        if u < 1/6:
            return 1
        elif u < 1/2:
            return 2
        elif u < 5/6:
            return 3
        else:
            return 4


    def update_areas(self):
        pass


    def generate_report(self):
        pass
