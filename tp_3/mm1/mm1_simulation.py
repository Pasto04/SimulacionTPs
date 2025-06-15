import numpy as np
from numpy.random import Generator, default_rng
from typing import Literal
from mm1.classes.statistical_counters import StatisticalCounters
from mm1.classes.system_state import SystemState
from mm1.classes.graphics import Graphics


class MM1Simulation:
    def __init__(self, arrival_rate, service_rate, sim_time=1000, max_queue=np.inf, random:Generator = default_rng()):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.sim_time = sim_time
        self.max_queue = max_queue
        self.random = random
        '''
        self.data = {
            'wait_times': [],
            'system_times': [],
            'blocked_customers': 0,
            'total_customers': 0,
        }
        '''


    def run_simulation(self):	
        self.init_simulation()      

        while self.clock < self.sim_time:
            event_type = self.advance_time()

            if (event_type == "arrival"):
                self.handle_arrival()
            else:
                self.handle_departure()
            self.system_state.last_event_time = self.clock
        
        #TODO self.update_area_under_b()
        #TODO self.update_area_under_q()
        self.generate_report()


    def init_simulation(self):
        self.clock = 0
        self.generate_next_arrival()
        self.next_departure_time = np.inf

        self.system_state= SystemState()
        self.statistical_counters = StatisticalCounters()


    def advance_time(self) -> Literal["arrival", "departure"]:
        if self.next_arrival_time < self.next_departure_time:
          self.clock = self.next_arrival_time
          return "arrival"
        else:
          self.clock = self.next_departure_time
          return "departure"


    def handle_arrival(self):
        self.generate_next_arrival()
        self.update_area_under_b()
        self.update_area_under_q()

        if self.system_state.server_busy == False:
            self.system_state.server_busy = True
            self.statistical_counters.customers_delayed += 1
            self.generate_next_departure()
            
            
        elif self.system_state.clients_in_queue < self.max_queue:
            self.system_state.clients_in_queue += 1
            self.system_state.arrival_times.append(self.clock)
            


    def handle_departure(self):
        self.update_area_under_b()
        self.update_area_under_q()
        
        if self.system_state.clients_in_queue == 0:
            self.system_state.server_busy = False
            self.next_departure_time = np.inf
        else:
            self.system_state.clients_in_queue -= 1
            self.statistical_counters.total_delay += self.calculate_customer_delay()
            self.statistical_counters.customers_delayed += 1
            self.generate_next_departure()



    def generate_next_arrival(self):
        self.next_arrival_time = self.clock + self.random.exponential(scale=1/self.arrival_rate)

    def generate_next_departure(self):
        self.next_departure_time = self.clock + self.random.exponential(scale=1/self.service_rate)


    def calculate_customer_delay(self):
        aux = self.system_state.arrival_times.pop(0)
        return self.clock - aux


    def update_area_under_b(self):
        if self.system_state.server_busy:
            time_since_last_event = self.clock - self.system_state.last_event_time
            self.statistical_counters.area_under_b += time_since_last_event


    def update_area_under_q(self):
        time_since_last_event = self.clock - self.system_state.last_event_time
        level = self.system_state.clients_in_queue

        if level not in self.statistical_counters.time_by_queue_level:
            self.statistical_counters.time_by_queue_level[level] = 0

        self.statistical_counters.time_by_queue_level[level] += time_since_last_event


    def generate_report(self):
        area_under_q = sum(
            int(level) * time for level, time in self.statistical_counters.time_by_queue_level.items()
        )
        average_customer_in_system = (area_under_q + self.statistical_counters.area_under_b) / self.sim_time
        average_customer_in_queue = area_under_q / self.sim_time
        average_time_in_system = self.statistical_counters.total_delay / self.statistical_counters.customers_delayed if self.statistical_counters.customers_delayed > 0 else 0
        average_time_in_queue = area_under_q / self.statistical_counters.customers_delayed if self.statistical_counters.customers_delayed > 0 else 0
        server_usage = self.statistical_counters.area_under_b / self.sim_time
        
        n_clients_in_queue_probability = {}
        for level, time in self.statistical_counters.time_by_queue_level.items():
            n_clients_in_queue_probability[level] = time / self.sim_time
        
        Graphics.generate_queue_probabilities_chart(n_clients_in_queue_probability)

        
        #TODO Probabilidad de denegación de servicio (cola finita de tamaño: 0, 2, 5, 10, 50).
