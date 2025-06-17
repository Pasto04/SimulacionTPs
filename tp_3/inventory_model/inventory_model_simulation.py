import numpy as np
from numpy.random import Generator, default_rng
from typing import Literal
from inventory_model.classes.report import InventoryModelReport
from inventory_model.classes.statistical_counters import StatisticalCounters
from inventory_model.classes.system_state import SystemState

class InventoryModelSimulation:
    def __init__(
        self,
        customer_arrival_rate: float,
        reorder_point: int,
        max_inventory_level: int,
        cost_per_unit: float,
        ordering_fixed_cost: float,
        holding_cost_per_unit_per_time: float,
        backorder_cost_per_unit_per_time: float,
        inventory_evaluation_period: float = 1,
        sim_time: float = 120,
        random: Generator = default_rng()
    ):
        self.customer_arrival_rate = customer_arrival_rate
        self.reorder_point = reorder_point
        self.max_inventory_level = max_inventory_level

        self.cost_per_unit = cost_per_unit
        self.ordering_fixed_cost = ordering_fixed_cost
        self.holding_cost_per_unit_per_time = holding_cost_per_unit_per_time
        self.backorder_cost_per_unit_per_time = backorder_cost_per_unit_per_time

        self.inventory_evaluation_period = inventory_evaluation_period
        self.sim_time = sim_time
        self.random = random


    def run_simulation(self) -> InventoryModelReport:
        self.init_simulation()
        event_type = self.advance_time()

        while self.clock < self.sim_time:
            if event_type == "customer_arrival":
                self.handle_customer_arrival()
            elif event_type == "order_arrival":
                self.handle_order_arrival()
            else:
                self.evaluate_inventory()

            self.system_state.last_event_time = self.clock
            event_type = self.advance_time()

        self.update_areas()
        return self.generate_report()


    def init_simulation(self):
        self.clock = 0
        self.generate_next_customer_arrival()
        self.next_order_arrival_time = np.inf
        self.next_inventory_evaluation_time = self.inventory_evaluation_period

        self.system_state = SystemState(self.reorder_point, self.max_inventory_level)
        self.statistical_counters = StatisticalCounters()


    def advance_time(self) -> Literal["customer_arrival", "order_arrival", "inventory_evaluation"]:
        event_times = {
            "customer_arrival": self.next_customer_arrival_time,
            "order_arrival": self.next_order_arrival_time,
            "inventory_evaluation": self.next_inventory_evaluation_time
        }

        next_event_type = min(event_times, key=event_times.get)
        self.clock = event_times[next_event_type]
        return next_event_type


    def handle_customer_arrival(self):
        self.update_areas()
        demand = self.generate_customer_demand()
        self.system_state.inventory_level -= demand
        self.generate_next_customer_arrival()


    def handle_order_arrival(self):
        self.update_areas()
        self.system_state.inventory_level += self.system_state.last_order_quantity
        self.system_state.last_order_quantity = 0
        self.next_order_arrival_time = np.inf


    def evaluate_inventory(self):
        if self.system_state.inventory_level < self.system_state.reorder_point:
            quantity = self.system_state.max_inventory_level - self.system_state.inventory_level
            self.system_state.last_order_quantity = quantity

            self.statistical_counters.total_ordering_cost += quantity * self.cost_per_unit + self.ordering_fixed_cost
            self.generate_next_order_arrival()

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


    def generate_next_order_arrival(self):
        self.next_order_arrival_time = self.clock + self.random.uniform(0.5, 1)


    def update_areas(self):
        level = self.system_state.inventory_level
        time = self.clock - self.system_state.last_event_time

        if level > 0:
            self.statistical_counters.area_under_available_inventory += level * time
        elif level < 0:
            self.statistical_counters.area_under_backordered_demand += -1 * level * time


    def generate_report(self) -> InventoryModelReport:
        ordering_cost = self.statistical_counters.total_ordering_cost
        holding_cost = self.statistical_counters.area_under_available_inventory * self.holding_cost_per_unit_per_time
        backorder_cost = self.statistical_counters.area_under_backordered_demand * self.backorder_cost_per_unit_per_time
        total_cost = ordering_cost + holding_cost + backorder_cost

        return InventoryModelReport(
            self.customer_arrival_rate,
            self.reorder_point,
            self.max_inventory_level,
            ordering_cost = ordering_cost / self.sim_time,
            holding_cost = holding_cost / self.sim_time,
            backorder_cost = backorder_cost / self.sim_time,
            total_cost = total_cost / self.sim_time
        )

