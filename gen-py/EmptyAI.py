#!/usr/bin/env python


from Proxy import Proxy
from command.WaitCommand import WaitCommand
from model.Plane import PlaneType

class EmptyAI:
    
    def __init__(self, ip, port):
        self.game = Proxy(ip, port, self)
        
    def think(self):
        # You're free to do everything you want here
        while True:
            self.game.update_sim_frame()
            
            for plane in self.game.get_my_planes():
                game.send_command(WaitCommand(p))

    def end(self):
        pass
        

if __name__ == "__main__":
    import sys
    
    # je sais pas ou mettre ca, desole :)
    
    
    MILITARY = PlaneType(0.7, 0.7, 100, 10, 10, 1, .03, 15)
    COMMERCIAL = PlaneType(0, MILITARY.radarRange, MILITARY.fullHealth*2, MILITARY.holdCapacity*5, MILITARY.tankCapacity*4, MILITARY.fuelConsumptionPerDistanceUnit*3, MILITARY.radius*2, 15)
    
    
    
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()
    
    ai = EmptyAI(sys.argv[1], int(sys.argv[2]))
    ai.think();