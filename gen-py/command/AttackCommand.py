from Command import Command

class AttackCommand(Command):
    
    def __init__(self, plane, target):
        Command.__init__(self)
        if p is None or target is None:
            raise Error("Attack Command :  null reference")
        self.planeSrc = plane
        self.planeTarget = target

    def __str__(self):
        return "attack " + self.planeSrc.get_id() + " -> " + self.planeTarget.get_id()
    
    def get_plane_src(self):
        return self.planeSrc
    
    def get_plane_target(self):
        return self.planeTarget