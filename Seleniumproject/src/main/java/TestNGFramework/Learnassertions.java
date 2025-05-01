package TestNGFramework;

import org.testng.Assert;
import org.testng.asserts.IAssert;
import org.testng.asserts.SoftAssert;

public class Learnassertions {
	public static void main(String[] args)
	{
		String s1 = "TestLeaf";
		String s2 = "TestLeaf";
		
		//Hard Asseertion stop at the point of failure 
		//Assert.assertEquals(s1, s2); //static
		
		//SoftAssertion will continue rill end of program
		
		SoftAssert softassert  = new SoftAssert();
		
		softassert.assertEquals(s1,s2);
		softassert.assertAll();//collect everythng all the assert mandatory to use this if not test will passs
		
	}

}
