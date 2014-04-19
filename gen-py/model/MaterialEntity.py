from Entity import Entity

class MaterialEntity(Entity):
    
    def __init__(self, id, coord, rotation, radar_range):
        Entity.__init__(self, id)
        self.position = coord
        self.rotation = rotation
        self.radar_range = radar_range
        
    def get_rotation(self):
        return self.rotation
    
    def get_position(self):
        return self.position
    
    def get_radar_range(self):
        return self.radar_range
    
    def rotate(self, angle):
        self.rotation += angle
        
    def set_position_x(self, x):
        self.position.set_x(x)
        
    def set_position_y(self, y):
        self.position.set_y(y)