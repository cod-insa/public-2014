package ai;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import model.*;
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
			catch(OutOfSyncException e) {
				System.out.println("Out of sync: "+e);
				System.err.println("Out of sync: "+e);
			}
			
			for (Command c: coms)
				game.sendCommand(c);
			
		}
		exit:
		in.close();
		game.quit(0);
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








