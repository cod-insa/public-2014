from Entity import Entity

class ProgressAxis(Entity):
    def __init__(self, id, base1, base2):
        Entity.__init__(self, id)
        self.base1 = base1
        self.base2 = base2
        self.length = base1.get_position().distanceTo(base2.get_position())
        
    def set_ration(self, ra1):
        self.ratio1 = ra1
        
    def set_ration(self, ra2):
        self.ratio1 = ra2
        
