from IncomingData import IncomingData
from CommandSender import CommandSender

from model.Base import Base
from model.Coord import Coord
from model.ProgressAxis import ProgressAxis
from model.Country import Country, Request
from model.Plane import Plane, PlaneType

from genbridge.ttypes import PlaneStateData

import sys


class Proxy:
    
    def __init__(self, ip, port, ai):
        self.client_ai = ai
        self.idm = IncomingData(ip, port, self)
        
        self.ai_planes= {}
        self.killed_planes = {}
        self.ennemy_planes= {}
        
        self.all_bases= {}
        self.ai_bases= {}
        self.other_visible_bases = {}
        self.other_notvisible_bases = {}
        
        self.map_axis = {}
        self.idm.retrieve_initial_data()
        
        self.player_id = self.idm.get_player_id()
        
        self.cm = CommandSender(ip, port+1, self.idm.get_id_connection(), self)
        self.cm.start()
    
    def set_init_data(self, data):
        for b in data.bases:
            base = Base(b.base_id, Coord(b.posit.x, b.posit.y))
            self.other_notvisible_bases[base.id] = base
            self.all_bases[base.id] = base
        
        self.map_width = data.mapWidth
        self.map_height = data.mapHeight
        
        for a in data.progressAxis:
            if a.base1_id in self.all_bases and a.base2_id in self.all_bases:
                self.map_axis[a.id] = ProgressAxis(a.id, self.all_bases[a.base1_id], self.all_bases[a.base2_id])
            else:
                print "One or both of the base " + str(a.base1_id) + " and " + str(a.base2_id) + " are unknown. Failed to add the axis"
         
        self.ai_country = Country(data.myCountry.country_id, Coord(data.myCountry.country.x, data.myCountry.country.y))
       
    def update_bases(self, data):
        def update_basic_infos(base, basedata):
            base.set_id(basedata.base_id)
        
        def update_full_infos(base, basedata):
            base.set_id(basedata.base_id)
            base.set_garrison(basedata.militarRessource)
            base.set_fuel(basedata.fuelRessource)
        
        self.ai_bases = {}
        self.other_notvisible_bases = {}
        self.other_visible_bases = {}
        
        for b in data.owned_bases:
            base_id = b.basic_info.base_id
            base = self.all_bases[base_id]
            if base is None:
                 raise Exception("The base with id " + str(base_id) + " does not exist")
             
            update_full_infos(base, b)
            self.ai_bases[base_id] = base
            
        for b in data.not_owned_visible_bases:
            base_id = b.basic_info.base_id
            base = all_bases[base_id]
            if base is None:
                 raise Exception("The base with id " + base_id + " does not exist")

            update_full_infos(base, b)
            self.other_visible_bases[base_id] = base
            
        for b in data.not_owned_not_visible_bases:
            base_id = b.base_id
            base = self.all_bases[base_id]
            if base is None:
                 raise Exception("The base with id " + base_id + " does not exist")

            update_basic_infos(base, b)
            self.other_notvisible_bases[base_id] = base        
    
    def update_planes(self, data):
   
        def state_converter(planestatedata):
            if planestatedata == PlaneStateData.AT_AIRPORT:
                s = Plane.AT_AIRPORT
            elif planestatedata == PlaneStateData.GOING_TO:
                s = Plane.GOING_TO
            elif planestatedata == PlaneStateData.ATTACKING:
                s = Plane.ATTACKING
            elif planestatedata == PlaneStateData.IDLE:
                s = Plane.IDLE
            elif planestatedata == PlaneStateData.DEAD:
                s = Plane.DEAD
            elif planestatedata == PlaneStateData.LANDING:
                s = Plane.LANDING
            elif planestatedata == PlaneStateData.FOLLOWING:
                s = Plane.FOLLOWING
            else:
                raise "Proxy : Unhandled Plane State"
            return s
    
        def update_basic_info(plane, planedata):
            plane.set_position_x(planedata.posit.x)
            plane.set_position_y(planedata.posit.y)
            plane.set_health(planedata.health)
            plane.set_owner_id(planedata.ai_id)
        
        def update_full_info(plane, planedata):
            update_basic_info(plane, planedata.basic_info)
            plane.set_fuel_in_tank(planedata.remainingGaz)
            plane.set_mil_in_hold(planedata.militarResourceCarried)
            plane.set_fuel_in_hold(planedata.fuelResourceCarried)
            plane.set_state(state_converter(planedata.state))
            if plane.get_state() == Plane.AT_AIRPORT:
                plane.assign_to(self.all_bases.get(planedata.base_id))
            else:
                plane.unassign()
        
        self.killed_planes.update(self.ai_planes)
        for p in self.ai_planes:
            self.ai_planes[p].set_exists(False)
        self.ai_planes = {}
        
        for p in data.owned_planes:
            if p.basic_info.ai_id != self.player_id:
                print "A not owned plane is in the owned ones: may generate errors"
            
            if p.basic_info.plane_id in self.killed_planes: #p is alive
                plane = self.killed_planes[p.basic_info.plane_id]
                del self.killed_planes[p.basic_info.plane_id]
                update_full_info(plane, p)
                self.ai_planes[p.basic_info.plane_id] = plane
            else:
                plane = Plane(p.basic_info.plane_id,Coord(p.basic_info.posit.x, p.basic_info.posit.y), PlaneType.get(p.basic_info.planeTypeId))
                plane.set_ai_object(True)
                update_full_info(plane, p)
                self.ai_planes[plane.get_id()] = plane
                
        for p in data.not_owned_planes:
            if p.ai_id != self.player_id:
                print "A owned plane is in the not owned ones: may generate errors"
            if p.plane_id in self.ennemy_planes:
                plane = self.ennemy_planes[p.plane_id]
                update_basic_info(plane, p)
            else: #First time that plane appear
                plane = Plane(p.plane_id, Coord.Unique(p.posit.x,p.posit.y), PlaneType.get(p.planeTypeId))
                plane.set_ai_object(True)
                update_basic_info(plane, p)
                self.ennemy_planes[plane.get_id()] = plane
                

    def update_axis(self, data):
        for a in data.progressAxis:
            if a.id in self.map_axis:
                prog_axis = map_axis[a.id]
                prog_axis.ratio1 = a.progressBase1
                prog_axis.ratio2 = a.progressBase2
                
    def update_country(self, data):
        for i in self.ai_country.get_production_line():
            if not i in data.productionLine:
                self.ai_country.get_production_line()[i].set_time(0)
                del self.ai_country.get_production_line()[i]
                
        for request_data in data.productionLine:
            if request_data.requestId in self.ai_country.get_production_line():
                self.ai_country.get_production_line()[request_data.requestId].set_time(request_data.timeBeforePlaneBuilt)
            else:
                self.ai_country.get_production_line()[rd.requestId] = Request(request_data.requestId, request_data.timeBeforePlaneBuilt, PlaneType.get(request_data.planeTypeId))
            
     
    def update_proxy_data(self, data):
        self.numframe = data.numFrame
        self.update_bases(data)
        self.update_planes(data)
        self.update_axis(data)
        self.update_country(data)  
    
    def get_num_frame(self):
        return self.numframe
    
    def get_map_width(self):
        return self.map_width
    
    def get_map_height(self):
        return self.map_height
    
    def get_killed_plane(self):
        return self.killed_planes
    
    def get_my_planes(self):
        return self.ai_planes
    
    def get_enemy_planes(selfs):
        return self.ennemy_planes
    
    def get_all_bases(self):
        return self.all_bases
    
    def get_my_bases(self):
        return self.ai_bases
    
    def get_not_owned_and_visible_bases(self):
        return self.other_visible_bases
    
    def get_not_owned_and_not_visible_bases(self):
        return self.other_notvisible_bases
    
    def get_country(self):
        return self.ai_country
    
    def is_time_out(self):
        return self.cm.is_time_out()
    
    def update_sim_frame(self):
        self.idm.update_data()
        
    def send_command(self, command):
        self.cm.send_command(command)        
        
    def quit(self, code):
        #if self.idm is not None:
        #    self.idm.terminate()
        #if self.client_ai is not None:
        #    self.client_ai.end()
        #if self.cm is not None:
        #    self.cm.terminate()
        #    try:
        #        cm.join()
        #    except:
        #        print tx.message
                
        sys.exit(code);
        