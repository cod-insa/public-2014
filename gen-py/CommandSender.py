from genbridge import CommandReceiver
from genbridge.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import threading 

from command import *

class CommandSender(threading.Thread):
    
    def __init__(self, ip, port, idc, proxy):
        threading.Thread.__init__(self)
        self.proxy = proxy
        self.running = False
        self.id_connection = idc
        self.is_time_out = False
        self.id_connection = idc
        self.waitingList = []
        self.my_lock = threading.Lock()
        self.my_event = threading.Event()
        
        try:
            transport = TSocket.TSocket(ip, port)
            transport.open()
            
            # transport = TTransport.TBufferedTransport(transport)
            
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            self.client = CommandReceiver.Client(protocol)

            transport.close()
        
        except Thrift.TException, tx:
          print "Error while connecting to the server. Message: " + tx.message + "\nCause : \
          The server is not running, the game may have begun, ended or, the port or the ip could be wrong"
    
    
    def run(self):
        self.running = True
        while self.running:
            with self.my_lock:
                while len(self.waitingList) == 0 and self.running:
                    self.my_event.wait()
                while len(self.waitingList) != 0 and self.running:
                    current_cmd = self.waitingList.pop(0)
                    self.send_thrift_command(current_cmd)
    
    def is_time_out(self):
        with self.my_lock:
            return self.is_time_out
        
    def send_command(self, command):
        with self.my_lock:
            self.waitingList.append(command)
            self.my_event.set()
            
    def send_thrift_command(self, cmd):
        print "Sending Command : "+str(cmd)
        r = None
        # MoveCommand
        if isinstance(cmd, command.MoveCommand):
            c = genbridge.ttypes.CoordData(cmd.get_destination().get_x(), cmd.get_destination().get_y())
            p = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane().get_id())
            r = self.client.sendMoveCommand(genbridge.ttypes.MoveCommandData(p, c), self.id_connection)
        # WaitCommand
        elif isinstance(cmd, command.WaitCommand):
            p = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane().get_id())
            r = self.client.sendWaitCommand(genbridge.ttypes.WaitCommandData(p), self.id_connection)
        #LandCommand
        elif isinstance(cmd, command.LandCommand):
            p = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane().get_id())
            r = self.client.sendLandCommand(genbridge.ttypes.LandCommandData(p, cmd.get_base.get_id()), self.id_connection)
        # AttackCommand
        elif isinstance(cmd, command.AttackCommand):
            p_src = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane_src().get_id())
            p_target = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane_target().get_id())
            r = self.client.sendAttackCommand(genbridge.ttypes.AttackCommandData(p_src, p_target), self.id_connection)
        # FollowCommand
        elif isinstance(cmd, command.FollowCommand):
            p_src = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane_src().get_id())
            p_target = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane_target().get_id())
            r = self.client.sendFollowCommand(genbridge.ttypes.FollowCommandData(p_src, p_target), self.id_connection)
        # DropMilitarsCommand
        elif isinstance(cmd, command.DropMilitarsCommand):
            p = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane().get_id())
            r = self.client.sendDropMilitarsCommand(genbridge.ttypes.DropMilitarsCommandData(p, cmd.get_base().get_id(), cmd.get_nbdrop()), self.id_connection)
        # FillFuelTankCommand
        elif isinstance(cmd, command.FillFuelTankCommand):
            p = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane().get_id())
            r = self.client.sendFillFuelTankCommand(genbridge.ttypes.FillFuelTankCommandData(p, cmd.get_quantity()), self.id_connection)
        # LoadRessourcesCommand
        elif isinstance(cmd, command.ExchangeResourcesCommand):
            p = genbridge.ttypes.PlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_plane().get_id())
            r = self.client.sendExchangeResourcesCommand(genbridge.ttypes.ExchangeResourcesCommandData(p, cmd.get_mil_qty(), cmd.get_fuel_qty(), cmd.get_delete_resources()), self.id_connection)
        # BuildPlaneCommand
        elif isinstance(cmd, command.BuildPlaneCommand):
            b = genbridge.ttypes.BuildPlaneCommandData(genbridge.ttypes.CommandData(self.proxy.get_num_frame()), cmd.get_requested_type().get_id())
            r = self.client.sendBuildPlaneCommand(b, self.id_connection)
        else:
            print "Unexpected error received while sending a command. Unknown command"
            self.proxy.quit(1);
        
        self.treat_result(r)
        
    def treat_result(self, r):
        if r.code == Command.SUCCESS:
            print "Command sent successfully !"
        elif r.code == Command.ERROR_TIME_OUT:
            print "Command is time out !"
        elif r.code == Command.WARNING_COMMAND:
            print "The command has been accepted but : "+ r.message
        else:
            print "The command has been ignored ! code:" + r.code + ", message: "+ r.message
    
    def new_frame(self):
        with self.my_lock:
            self.is_time_out = False
    
    def terminate(self):
        self.running = False;
        with self.my_lock:
            self.my_event.set()