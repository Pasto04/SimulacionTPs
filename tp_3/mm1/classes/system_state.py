class SystemState:
    def __init__(self):
        self.server_busy = False
        self.clients_in_queue = 0
        self.arrival_times = []
        self.last_event_time = 0
