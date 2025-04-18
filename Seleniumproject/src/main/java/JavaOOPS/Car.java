package JavaOOPS;

public class Car extends Vehicle {
	public void car()
	{
		System.out.println("Iam driving a car!");
	}
	public static void main(String[] args)
	{
		Car mycar = new Car();
		mycar.car();
		mycar.drive();
		mycar.brake();
		
	}

}
