from Command import Command

class MoveCommand(Command):

    def __init__(self, plane, coord):
        Command.__init__(self)
        if plane is None:
            raise "MoveCommand : null reference"
        self.plane = plane
        self.destination = coord

    def get_plane(self):
        return self.plane
    
    def get_destination(self):
        return self.destination

    def __str__(self):
        return "mv "+self.plane.get_id()+" -> "+str(coord)
