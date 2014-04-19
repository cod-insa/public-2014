from Command import Command

class LandCommand(Command):
    def __init__(self, plane, base):
        Command.__init__(self)
        if base is None or plane is None:
            raise "LandCommand : null reference"
        self.plane = plane
        self.base = base

    def get_plane(self):
        return self.plane
    
    def get_base(self):
        return self.base
    
    def __str__(self):
        return "land " + self.plane.get_id() + " -> " + self.base.get_id()

