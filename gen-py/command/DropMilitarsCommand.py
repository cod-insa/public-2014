from Command import Command

class DropMilitarsCommand(Command):
    
    def __init__(self, plane, base, nb_drop):
        Command.__init__(self)
        if plane is None or base is None:
            raise "DropMilitarsCommand : Null reference"
        self.planeSrc = plane
        self.baseTarget = base
        self.quantity = nb_drop

    def __str__(self):
        return "drop " + self.planeSrc.get_id() + " --(" + self.quantity + ")--> " + self.baseTarget.get_id()
    
    def get_plane(self):
        return self.plane
    
    def get_base(self):
        return self.base
    
    def get_nbdrop(self):
        return self.nbdrop
