from MaterialEntity import MaterialEntity

class AbstractBase(MaterialEntity):
    
    def __init__(self, id, coord):
        self.id = id
        self.position = coord
        self.planes = []
        
        
    def remove_plane(self, plane):
        if p in self.planes:
            self.planes.remove(p)
        else:
            raise Error("AbstractBase : Try to remove a plane not in base or country")
        
    def add_plane(self, plane):
        self.planes.append(plane)