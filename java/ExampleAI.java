package ai;


public class ExampleAI extends AbstractAI 
{
	
	public ExampleAI(String ip, int port)
	{
		super(ip,port);
	}

	@Override
	public void think() {
		
		while (true) {
			game.updateSimFrame();
			
			// Do your stuff here
			
			// Send your command whenever you want with game.sendCommand(new ...Command(...));
			
			// Be carefull not to be timed out. If this is the case, your algorithm is too slow...
		}
	}
	
	public static void main(String[] args) 
	{
		if (args.length != 2)
		{
			System.out.println("Usage : java AttackAI ip port");
			System.exit(1);
		}
		String ip = args[0];
		int port = Integer.parseInt(args[1]);
		
		AbstractAI ai = new ExampleAI(ip,port);
		ai.think();
	}
}








