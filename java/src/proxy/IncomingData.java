package proxy;

import genbridge.Bridge;
import genbridge.ConnectionData;
import genbridge.Data;
import genbridge.InitData;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;

public class IncomingData {

	private Proxy proxy;
	private int connection_id;
	private int player_id;


	private Bridge.Client client;
	
	public IncomingData(String ip, int port, Proxy p)
	{
		proxy = p;
		// Initialize client
		try 
		{
			// Initialize Socket of client
	    	TTransport transport;
	    	transport = new TSocket(ip, port);
	    	transport.open();
	    	
	    	TProtocol protocol = new  TBinaryProtocol(transport);
	    	client = new Bridge.Client(protocol);
	      
	    } catch (Exception e) {
	    	Proxy.log.error("Error while connecting to the server. Message: " + e.getMessage() + "\nCause : The server is not running, the game may have begun, ended or, the port or the ip could be wrong");
	    	proxy.quit(1);
	    }
	}
	
	
	public int getIdConnection() {
		return connection_id;
	}
	public int getPlayerId() {
		return player_id;
	}
	
	public void retrieveInitialData()
	{
		try 
		{
			ConnectionData cd = client.connect("Banane2");
			player_id = cd.player_id;
			connection_id = cd.con_id;
			
			if (connection_id < 0)
			{
				Proxy.log.error("Error while connecting to the server.\nCause : Id returned by server is invalid.");
				proxy.quit(2);
			}
			else
				Proxy.log.debug("Connected with id: " + connection_id + ". You are player n°" + player_id);
			
			Proxy.log.debug("Retrieving initial data");
			InitData d = client.retrieveInitData(connection_id);
			
			proxy.setInitData(d);
			
		} catch (TException e) {
			Proxy.log.error("Unexpected error while retrieving initial data from server. Message: " + e.getMessage());
			
			proxy.quit(3);
		}
	}
	
	public void updateData()
	{
		try {
			Data d = client.retrieveData(connection_id); // Will be blocked during call
			if (d.numFrame < 0)
			{
				if (d.numFrame == -1)
				{
					Proxy.log.debug("Received an end-of-game frame id (-1), stopping.");
					proxy.quit(0);
				}
				else 
				{
					Proxy.log.warn("Error: frame sent by the server is not valid (number "+d.numFrame+"). Ignoring");
					proxy.quit(4); 
				}
			}
			else
				proxy.updateProxyData(d);

		} catch (TException e) {
			Proxy.log.error("Unexpected error while retrieving data from server. Message: " + e.getMessage());
			proxy.quit(3);
		}
	}


	public void terminate() {
		if (client.getInputProtocol().getTransport().isOpen())
			client.getInputProtocol().getTransport().close();
		if (client.getOutputProtocol().getTransport().isOpen())
			client.getOutputProtocol().getTransport().close();
	}
}








