package ai;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import model.AbstractBase;
import model.Base;
import model.Coord;
import model.Plane;
import model.Plane.BasicView;
import command.AttackCommand;
import command.Command;
import command.DropMilitarsCommand;
import command.LandCommand;
import command.MoveCommand;
import common.MapView;

public class ConsoleAI extends AbstractAI 
{
	
	public ConsoleAI(String ip, int port)
	{
		super(ip,port);
	}

	@Override
	public void think() {
		think_blocking();
	}
	
	public void think_blocking() {
		Scanner in = new Scanner(System.in);
		
		main_loop:
		while (true) {

			System.out.print("Next action ([move|land|attk] id; list; exit): ");
			
			String[] cmd = in.nextLine().split(" ");

			System.out.print("Processing command... ");
			System.out.flush();
			
			game.updateSimFrame();
			

			MapView<Integer, Base.BasicView> bases;
			MapView<Integer, Plane.FullView> planes;
			MapView<Integer, BasicView> ennemy_planes;	

			bases = game.getAllBases();
			planes = game.getMyPlanes();
			ennemy_planes = game.getEnnemyPlanes();
			
			List<Command> coms = new ArrayList<>();
			
			try {
				boolean recognized = true;
				switch(cmd[0]) {
					case "exit":
						break main_loop;
					case "move": {
						if (cmd.length == 2)
						{
							int id = Integer.parseInt(cmd[1]);
							Base.BasicView b = bases.get(id);
							Coord.View c = null;
							
							if (b == null)
								if (game.getCountry().id() != id)
								{
									System.err.println("This id isn't corresponding neither to a base nor your country");
									break;
								}
								else
									c = game.getCountry().position();
							else
								c = b.position();
							
							for (Plane.FullView p: planes.valuesView())
								coms.add(new MoveCommand(p, c));
						}
						break;
					}
					case "land": {
						int id = Integer.parseInt(cmd[1]);
						Base.BasicView b = bases.get(id);
						AbstractBase.View c = null;
						
						if (b == null)
							if (game.getCountry().id() != id)
							{
								System.err.println("You can't see this base, move around it before you land");
								break;
							}
							else
								c = game.getCountry();
						else
							c = b;
						
						for (Plane.FullView p: planes.valuesView())
							coms.add(new LandCommand(p, c));
						
						break;
					}
					case "attk":
						Plane.BasicView ep = ennemy_planes.get(Integer.parseInt(cmd[1]));
						if (ep == null)
						{
							System.err.println("Bad id, this plane does not exists");
							break;
						}
						for (Plane.FullView p : planes.valuesView())
							coms.add(new AttackCommand(p, ep));
						break;
					case "list":
						System.out.println();
						System.out.println(">> My planes:");
						for (Plane.FullView p : planes.valuesView())
							System.out.println(p);
						System.out.println(">> Ennemy planes:");
						for (Plane.BasicView p : ennemy_planes.valuesView())
							System.out.println(p);
						System.out.println(">> Visible bases :");
						for (Base.FullView b : game.getVisibleBase().valuesView())
							System.out.println(b);
						System.out.println(">> Your Country");
						System.out.println(game.getCountry());
						break;
					default:
						recognized = false;
						System.err.println("Unrecognized command!");
				}
				if (recognized)
					System.out.println("Processed");
			}
			catch(IllegalArgumentException e) {
				System.out.println("Command failed: "+e);
				System.err.println("Command failed: "+e);
			}
			
			for (Command c: coms)
				game.sendCommand(c);
			
		}
		exit:
		in.close();
		game.quit(0);
	}
	
	public void think_async() {
		Scanner in = new Scanner(System.in);
		//int lastNumFrame = -1;

		class Updater extends Thread {
			public volatile boolean active = true;
			
			@Override
			public void run() {
				while (active) {
					synchronized (this) {
						game.updateSimFrame();
//						System.out.println("updated");
						
					}
				}
			}
		};
		final Updater updater = new Updater();
		updater.start();
		
		main_loop:
		while (true) {
//			game.updateSimFrame();
//			ArrayList<Base.View> bases = game.getBases();

//			if (lastNumFrame != game.getNumFrame()) {
//				game.updateSimFrame();
//				lastNumFrame = game.getNumFrame();
//			}
			//int i;

			System.out.print("Next action ([move|land|attk] id; exit to quit): ");
			//i = in.nextInt();
			
			String[] cmd = in.nextLine().split(" ");

			MapView<Integer, Base.BasicView> bases;
			MapView<Integer, Plane.FullView> planes;
			MapView<Integer, BasicView> ennemy_planes;

//			System.out.println("waiting");
			
			// TODO FIXME! there should be synchronization but it doesn't work!
//			synchronized (updater) {
				bases = game.getAllBases();
				planes = game.getMyPlanes();
				ennemy_planes = game.getEnnemyPlanes();
//			}

//			System.out.println("sync");
			
			List<Command> coms = new ArrayList<>();
			
			switch(cmd[0]) {
				case "exit":
					break main_loop;
				case "move": {
					Base.BasicView b = bases.get(Integer.parseInt(cmd[1]));
					for (Plane.FullView p: planes.valuesView())
						coms.add(new MoveCommand(p, b.position()));
					break;
				}
				case "land": {
					Base.BasicView b = bases.get(Integer.parseInt(cmd[1]));
					if (b instanceof Base.FullView)
						for (Plane.FullView p : planes.valuesView())
							coms.add(new LandCommand(p, (Base.FullView)b));
					else
						System.err.println("You can't see this base, move around it before you land");
					break;
				}
				case "attk":
					for (Plane.FullView p : planes.valuesView())
						coms.add(new AttackCommand(p, ennemy_planes.get(Integer.parseInt(cmd[1]))));
					break;
				default:
					System.err.println("Unrecognized command!");
			}
			
			for (Command c: coms)
				game.sendCommand(c);

			


//			if (i < 0) {
//				//in.close();
//				/* I want to */ break /* free! */;
//			}
//			
//			Base.View b = bases.get(i);
//			
//			for (Plane.FullView p : game.getMyPlanes())
//			{
//				MoveCommand mc = new MoveCommand(p.id(), b.position());
//				
//				System.out.println("Sending command "+mc);
//				
//				game.sendCommand(mc);
//			}
		}
		exit:
		in.close();
		updater.active = false;
		try {
			updater.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) throws InterruptedException {
		if (args.length != 2)
		{
			System.out.println("Usage : java MoveAI ip port");
			System.exit(1);
		}
		String ip = args[0];
		int port = Integer.parseInt(args[1]);
		
		AbstractAI ai = new ConsoleAI(ip,port);
		ai.think();
	}

}








