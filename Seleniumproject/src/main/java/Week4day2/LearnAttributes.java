package Week4day2;

import org.testng.annotations.Test;

public class LearnAttributes {
	@Test(priority= -1,enabled = false) // it will ignore from execution
	public void createLead()
	{
		System.out.println("CreateLead");
		
	}
	@Test(priority  = -1,invocationCount =5,dependsOnMethods = {"createLead"}) /// will run 5 times 
	public void editLead()
	{
		System.out.println("EditLeadt");
		
	}
	@Test
	public void deleteLead()
	
	{
		
		System.out.println("Delete lad");
	}

}
