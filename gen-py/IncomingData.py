from genbridge import Bridge
from genbridge.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class IncomingData:
    
    def __init__(self, ip, port, proxy):
        self.proxy = proxy
        
        try:
            transport = TSocket.TSocket(ip, port)
            transport.open()
            
            # transport = TTransport.TBufferedTransport(transport)
            
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            self.client = Bridge.Client(protocol)
        
        except Thrift.TException, tx:
          print "Error while connecting to the server. Message: " + tx.message + "\nCause : \
          The server is not running, the game may have begun, ended or, the port or the ip could be wrong"
          self.proxy.quit(1)
          
    def get_id_connection(self):
        return self.connection_id
    
    def get_player_id(self):
        return self.player_id
    
    def retrieve_initial_data(self):
        
        try:
            connection_data = self.client.connect("Banane2")
            self.player_id = connection_data.player_id
            self.connection_id = connection_data.con_id
            
            if self.connection_id < 0:
                print "Error while connecting to the server.\nCause : Id returned by server is invalid."
                self.proxy.quit(2)
            else:
                print "Connected with id: " + str(self.connection_id) + ". You are player n" + str(self.player_id)
                
            print "Retrieving initial data"
            
            init_data = self.client.retrieveInitData(self.connection_id)
            
            self.proxy.set_init_data(init_data)
            
        except Thrift.TException, tx:
            print "Unexpected error while retrieving initial data from server. Message: " + tx.message
            self.proxy.quit(3)
            
    def update_data(self):
        try:
            data = self.client.retrieveData(self.connection_id)
            
            if data.numFrame < 0:
                if data.numFrame == -1:
                    print "Received an end-of-game frame id (-1), stopping."
                    self.proxy.quit(0)
                else:
                    print "Error: frame sent by the server is not valid (number "+str(data.numFrame)+"). Ignoring"
                    self.proxy.quit(4)
                    
            self.proxy.update_proxy_data(data)
            
        except Thrift.TException, tx:
            print "Unexpected error while retrieving data from server. Message: " + tx.message
            self.proxy.quit(3)


    def terminate(self):
        if self.client.getInputProtocol().getTransport().isOpen():
            self.client.getInputProtocol().getTransport().close()
        if self.client.getOutputProtocol().getTransport().isOpen():
            self.client.getOutputProtocol().getTransport().close()