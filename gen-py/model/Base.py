from AbstractBase import AbstractBase

class Base(AbstractBase):
    
    def __init__(self, id, coord):
        AbstractBase.__init__(self, id, coord)
        self.militaryGarrison = 0
        self.fuelInStock = 0
        
    def get_position(self):
        return self.position
    
    def get_militaryGarrison(self):
        return self.militaryGarrison
    
    def get_fuelInStock(self):
        return self.fuelInStock
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def set_garrison(self, nb):
        self.militaryGarrison = nb
        
    def set_fuel(self, nb):
        self.fuelInStock = nb