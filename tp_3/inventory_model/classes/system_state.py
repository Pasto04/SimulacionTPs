class SystemState:
    def __init__(self):
        self.inventory_level = 20 #TODO permitir que se modifique
        self.available_inventory = 20
        self.backordered_demand = 0
        
        self.last_order_quantity = 0
        self.reorder_point = 15
        self.max_inventory_level = 30
