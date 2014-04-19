from Command import Command

class ExchangeResourcesCommand(Command):
    def __init__(self, plane, mil_qty, fuel_qty, delete):
        Command.__init__(self)
        if plane is None:
            raise "LoadRessourcesCommand : Null reference"
        self.planeSrc = plane
        self.militarQuantity = mil_qty
        self.fuelQuantity = fuel_qty
        self.delete_ressources = delete

    def __str__(self):
        return "loadResource " + self.planeSrc.get_id() + " : militar => " + self.militarQuantity + "; fuel => " + self.fuelQuantity

    def get_plane(self):
        return self.plane
    
    def get_fuel_qty(self):
        return self.fuelQuantity
    
    def get_mil_qty(self):
        return self.militarQuantity

    def get_delete_resources(self):
        return self.delete_ressources