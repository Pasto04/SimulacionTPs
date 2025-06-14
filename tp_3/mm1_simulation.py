import random
import numpy as np
from typing import Literal

class MM1Simulation:
    def _init_(self, arrival_rate, service_rate, sim_time=1000, max_queue=np.inf, random = np.random.default_rng(seed=1234)):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.sim_time = sim_time
        self.max_queue = max_queue
        self.random = random
        self.data = {
            'wait_times': [],
            'system_times': [],
            'blocked_customers': 0,
            'total_customers': 0,
        }

    
    def run_simulation(self):
        self.init_simulation()      
        event_type = self.advance_time()

        #TODO chequear que no hyaa terminado
        if (event_type == "arrival"):
          self.handle_arrival()
        else:
          self.handle_departure()
        

    def init_simulation(self):
      self.clock = 0
      #inicializar estado del sistema y contadores estadísticos. ver qué hacer
      self.next_arrival = self.random.exponential(scale=self.arrival_rate)
      self.next_departure = np.inf


    def advance_time(self) -> Literal["arrival", "departure"]:
        if self.next_arrival < self.next_departure:
          self.clock = self.next_arrival
          return "arrival"
        else:
          self.clock = self.next_departure
          return "departure"



    def handle_arrival():
      # si está libre, ocupar el servidor
      # si no actializar cant en cola
      # 
      pass


    def handle_departure():
        pass


    


    def generate_report():
        pass
