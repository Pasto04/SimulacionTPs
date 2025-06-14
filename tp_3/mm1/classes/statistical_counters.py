class StatisticalCounters:
    def __init__(self):
        self.customers_delayed = 0
        self.total_delay = 0
        self.time_by_queue_level = {0: 0}
        self.area_under_b = 0
