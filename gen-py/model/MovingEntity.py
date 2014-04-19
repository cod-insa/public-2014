from MaterialEntity import MaterialEntity

class MovingEntity(MaterialEntity):
    
    def __init__(self, id, coord, rotation=0, radar_range=0, inertia=0):
        MaterialEntity.__init(self, id, coord, rotation, radar_range)
        self.inertia = inertia