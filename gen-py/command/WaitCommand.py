from Command import Command

class WaitCommand(Command):

    def __init__(self, plane):
        Command.__init__(self)
        if plane is None:
            raise "WaitCommand : null reference"
        self.plane = plane
        
    def get_plane(self):
        return self.plane
    
    def __str__(self):
        return "wait " + self.plane.get_id()
