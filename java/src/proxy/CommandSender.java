package proxy;

import genbridge.AttackCommandData;
import genbridge.BuildPlaneCommandData;
import genbridge.CancelBuildRequestCommandData;
import genbridge.CommandData;
import genbridge.CommandReceiver;
import genbridge.CoordData;
import genbridge.DropMilitarsCommandData;
import genbridge.ExchangeResourcesCommandData;
import genbridge.FillFuelTankCommandData;
import genbridge.FollowCommandData;
import genbridge.LandCommandData;
import genbridge.MoveCommandData;
import genbridge.PlaneCommandData;
import genbridge.Response;
import genbridge.WaitCommandData;

import java.util.LinkedList;
import java.util.Queue;

import model.Coord;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;

import command.AttackCommand;
import command.BuildPlaneCommand;
import command.CancelRequestCommand;
import command.Command;
import command.DropMilitarsCommand;
import command.ExchangeResourcesCommand;
import command.FillFuelTankCommand;
import command.FollowCommand;
import command.LandCommand;
import command.MoveCommand;
import command.WaitCommand;

public class CommandSender extends Thread {

	private CommandReceiver.Client client;
	private boolean isTimeOut;
	private int idConnection;
	private Proxy proxy;
	private boolean running;

	private Queue<Command> waitingList;

	public CommandSender(String ip, int port, int idC, Proxy p) {
		proxy = p;
		running = false;
		waitingList = new LinkedList<Command>();
		isTimeOut = false;
		idConnection = idC;

		// Initialize client
		try {
			// Initialize Socket of client
			TTransport transport;
			transport = new TSocket(ip, port);
			transport.open();

			TProtocol protocol = new TBinaryProtocol(transport);
			// TProtocol protocol = new TSimpleJSONProtocol(transport);

			client = new CommandReceiver.Client(protocol);

		} catch (Exception e) {
			Proxy.log.error("Error while connecting to the server. Message: "
							+ e.getMessage() + "\nCause : The server is not running, the game may have ended or, the port or the ip may be not good");
			proxy.quit(1);
		}
	}

	public synchronized boolean isTimeOut() {
		return isTimeOut;
	}

	public synchronized void newFrame() {
		isTimeOut = false;
	}

	@Override
	public void run() {
		running = true;
		Command currentCmd;
		while (running) {
			synchronized (this) {
				while (waitingList.isEmpty() && running) {
					try {
						// Proxy.log.debug(">> waiting");
						wait();
						// Proxy.log.debug(">> notified");
					} catch (InterruptedException ie) {
						ie.printStackTrace();
					}
				}
				while (!waitingList.isEmpty() && running) {
					currentCmd = waitingList.remove();
					sendThriftCommand(currentCmd);
					// Proxy.log.debug(">> sent");
				}
			}
		}
		if (client.getInputProtocol().getTransport().isOpen())
			client.getInputProtocol().getTransport().close();
		if (client.getOutputProtocol().getTransport().isOpen())
			client.getOutputProtocol().getTransport().close();
	}

	public synchronized void sendCommand(Command cmd) {
		waitingList.add(cmd);
		notify();
	}

	private void sendThriftCommand(Command cmd) {
		Proxy.log.debug("Sending command : " + cmd);
		Response r = null;
		try {
			try { // match the command
				cmd.match();
			} catch (MoveCommand c) {
				// Call server method
				r = client.sendMoveCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (WaitCommand c) {
				// Call server method
				r = client.sendWaitCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (LandCommand c) {
				// Call server method
				r = client.sendLandCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (AttackCommand c) {
				r = client.sendAttackCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (FollowCommand c) {
				r = client.sendFollowCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (DropMilitarsCommand c) {
				r = client.sendDropMilitarsCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (FillFuelTankCommand c) {
				r = client.sendFillFuelTankCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (ExchangeResourcesCommand c) {
				r = client.sendExchangeResourcesCommandData(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (BuildPlaneCommand c) {
				r = client.sendBuildPlaneCommand(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			} catch (CancelRequestCommand c) {
				r = client.sendCancelBuildRequestCommandData(
						DataMaker.make(c, proxy.getNumFrame()), idConnection);
			}
			
			treatResult(r);
		} catch (TException e) {
			Proxy.log
					.error("Unexpected error received while sending a command. Message: "
							+ e.getMessage());
			e.printStackTrace();
			proxy.quit(1);
		}
	}
	
	private void treatResult(Response r) {

		switch (r.code) {
		case Command.SUCCESS:
			Proxy.log.debug("Command sent successfully !");
			break;
		case Command.ERROR_TIME_OUT:
			isTimeOut = true;
			Proxy.log.warn("Command is time out !");
			break;
		case Command.WARNING_COMMAND:
			Proxy.log.warn("The command has been accepted but : " + r.message);
			break;
		default:
			Proxy.log.warn("The command has been ignored ! code:" + r.code + ", message: "
					+ r.message);
		}
	}

	public void terminate() {
		running = false;
		synchronized(this)
		{
			notify();
		}
	}

	public static class DataMaker {

		static CoordData make(Coord.View c) {
			return new CoordData(c.x(), c.y());
		}

		public static BuildPlaneCommandData make(BuildPlaneCommand c,
				int numFrame) {
					return new BuildPlaneCommandData(new CommandData(numFrame), c.requestedType.id);
		}

		static LandCommandData make(LandCommand cmd, int numFrame) {
			return new LandCommandData(new PlaneCommandData(new CommandData(
					numFrame), cmd.plane.id()), cmd.base.id());
		}

		static AttackCommandData make(AttackCommand cmd, int numFrame) {
			return new AttackCommandData(new PlaneCommandData(new CommandData(
					numFrame), cmd.planeSrc.id()), cmd.planeTarget.id());
		}
		
		static FollowCommandData make(FollowCommand cmd, int numFrame) {
			return new FollowCommandData(new PlaneCommandData(new CommandData(
					numFrame), cmd.planeSrc.id()), cmd.planeTarget.id());
		}
		
		static MoveCommandData make(MoveCommand cmd, int numFrame) {
			return new MoveCommandData(new PlaneCommandData(new CommandData(
					numFrame), cmd.plane.id()), make(cmd.destination.view));
		}

		static WaitCommandData make(WaitCommand cmd, int numFrame) {
			return new WaitCommandData(new PlaneCommandData(new CommandData(
					numFrame), cmd.plane.id()));
		}
		
		static DropMilitarsCommandData make(DropMilitarsCommand cmd, int numFrame) {
			return new DropMilitarsCommandData(new PlaneCommandData(new CommandData(
					numFrame),cmd.planeSrc.id()), cmd.baseTarget.id(), cmd.quantity);
		}
		
		static FillFuelTankCommandData make(FillFuelTankCommand cmd, int numFrame) {
			return new FillFuelTankCommandData(new PlaneCommandData(new CommandData(
					numFrame),cmd.planeSrc.id()),cmd.quantity); 
		}
		
		static ExchangeResourcesCommandData make(ExchangeResourcesCommand cmd, int numFrame) {
			return new ExchangeResourcesCommandData(new PlaneCommandData(new CommandData(
					numFrame),cmd.planeSrc.id()),cmd.militarQuantity, cmd.fuelQuantity, cmd.deleteResources); 
		}
		
		static CancelBuildRequestCommandData make(CancelRequestCommand c,
				int numFrame) {
			return new CancelBuildRequestCommandData(new CommandData(numFrame), c.request.rqId());
		}
	}
}
