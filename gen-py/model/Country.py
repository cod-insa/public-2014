from AbstractBase import AbstractBase

class Country(AbstractBase):
    
    def __init__(self, id, coord):
        AbstractBase.__init__(self, id, coord)
        self.production_line = {} #contains (id, request)
        
    def line_full(self):
        return len(production_line) == 0
    
    def get_production_line(self):
        return self.production_line
    
class Request:
    
    def __init__(self, id, time, plane_type):
        self.id = id
        self.time = time
        self.plane_type = plane_type
        
    def set_time(self, time):
        self.time = time