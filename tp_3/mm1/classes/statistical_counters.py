class StatisticalCounters:
    def __init__(self):
        self.customers_delayed = 0
        self.total_delay = 0
        self.time_by_queue_level = {0: 0.0}
        self.area_under_b = 0
        self.total_arrivals = 0
        self.blocking_counts = {0:0, 2:0, 5:0, 10:0, 50:0}

