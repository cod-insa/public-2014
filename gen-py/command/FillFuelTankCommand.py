import model.Plane
from Command import Command

class FillFuelTankCommand(Command):
    planeSrc = Plane.FullView()
    quantity = float()

    def __init__(self, plane, quantity_fuel):
        Command.__init__(self)
        if plane is None:
            raise "FillFuelTankCommand : Null reference"
        self.planeSrc = plane
        self.quantity = quantity_fuel

    def __str__(self):
        return "store " + self.planeSrc.get_id() + " :> " + self.quantity
    
    def get_plane(self):
        return self.plane
    
    def get_nbdrop(self):
        return self.nbdrop

