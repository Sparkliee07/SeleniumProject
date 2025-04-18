package JavaOOPS;

public class Bike extends Car{

	public void vroom()
	{
		System.out.print("Vroom vroom");
	}
	public static void main(String[] args)
	{
		Bike bike = new Bike ();
		bike.vroom();
		bike.car();
		bike.drive();
		bike.brake();
	}
}


