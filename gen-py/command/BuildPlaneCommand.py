from Command import Command

class BuildPlaneCommand(Command):

    def __init__(self, requestedType):
        Command.__init__(self)
        if requestedType is None:
            raise "BuildPlaneCommande : null reference"
        self.requestedType = requestedType

    def __str__(self):
        return "build " + ("military" if self.requestedType == Plane.Type.MILITARY else "commercial")
    
    def get_requested_type(self):
        return self.requestedType

