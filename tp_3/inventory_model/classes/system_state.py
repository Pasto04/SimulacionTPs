class SystemState:
    def __init__(self, reorder_point: int = 15, max_inventory_level: int = 30):
        self.inventory_level = 20
        self.available_inventory = 20
        self.backordered_demand = 0
        
        self.last_event_time = 0
        self.last_order_quantity = 0
        
        self.reorder_point = reorder_point
        self.max_inventory_level = max_inventory_level
