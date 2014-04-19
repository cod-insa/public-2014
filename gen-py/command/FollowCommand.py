from Command import Command

class FollowCommand(Command):

    def __init__(self, plane, target):
        Command.__init__(self)
        if plane is None or target is None:
            raise "FollowCommand : null reference"
        self.planeSrc = plane
        self.planeTarget = target

    def __str__(self):
        return "follow " + self.planeSrc.get_id() + " -> " + self.planeTarget._id()

    def get_plane_src(self):
        return self.planeSrc
    
    def get_plane_target(self):
        return self.planeTarget