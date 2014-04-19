from MovingEntity import MovingEntity
import sys

class Plane(MovingEntity):
    IDLE = 1
    GOING_TO = 2
    FOLLOWING = 3
    ATTACKING = 4
    LANDING = 5
    AT_AIRPORT = 6
    DEAD = 7
    
    def __init__(self, id, coord, type):
        self.id = id
        self.position = coord
        self.type = type
        self.cur_base = None
    
    def set_health(self, health):
        self.health = health
        
    def get_health(self):
        return self.health
    
    def set_fuel_in_tank(self, fuel):
        self.fuel_in_tank = fuel
        
    def get_fuel_in_tank(self):
        return self.fuel_in_tank
    
    # Cargaison
    def set_fuel_in_hold(self, fuel):
        self.fuel_in_hold = fuel
    
    def get_fuel_in_hold(self, fuel):
        return self.fuel_in_hold
    
    def set_mil_in_hold(self, mil):
        self.military_in_hold = mil
    
    def get_mil_in_hold(self):
        return self.military_in_hold
    
    def set_state(self, s):
        self.state = s
        
    def get_state(self):
        return self.state
    
    def assign_to(self, base):
        self.unassign()
        self.cur_base = base
        if base is None:
            print "Plane : Null_reference for base"
            #sys.exit(0)
        base.add_plane(self)
        if base.get_owner_id() != self.get_owner_id():
            raise AssertionError("Plane assginement error")
        
    def unassign(self):
        if self.cur_base is not None:
            self.cur_base.remove_plane(self)
            self.cur_base = None
    
    def get_base(self):
        return self.cur_base
    
    def set_base(self, base):
        self.cur_base = base
    
class PlaneType:
    
    INSTANCES = []
    REGEN_SPEED = 0.1
  
    def __init__(self, firingRange, radarRange, fullHealth, holdCapacity, tankCapacity, fuelConsumptionPerDistanceUnit, radius, timeToBuild):
        self.firingRange = firingRange
        self.radarRange = radarRange
        self.fullHealth = fullHealth
        self.holdCapacity = holdCapacity
        self.tankCapacity = tankCapacity
        self.fuelConsumptionPerDistanceUnit = fuelConsumptionPerDistanceUnit
        self.radius = radius
        self.timeToBuild = timeToBuild
        
        id = len(self.INSTANCES)
        
        self.INSTANCES.append(self)
    
    @staticmethod
    def get(id):
        return PlaneType.INSTANCES[id]
    
    