package Week4day2;

import org.testng.annotations.Test;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.AfterSuite;

public class LearnAnnotations {
  @Test
  public void createLead() {
	  System.out.println("creat nmethod");
  }
  @Test
  public void editLead() {
	  System.out.println("edit nmethod");
  }
  @Test
  public void deleteLead() {
	  System.out.println("delete nmethod");
  }
  @BeforeMethod
  public void beforeMethod() {
	  System.out.println("before nmethod");
  }

  @AfterMethod
  public void afterMethod() {
	  System.out.println("false");
  }

  @BeforeClass
  public void beforeClass() {
  }

  @AfterClass
  public void afterClass() {
  }

  @BeforeTest
  public void beforeTest() {
  }

  @AfterTest
  public void afterTest() {				
  }

  @BeforeSuite
  public void beforeSuite() {
	  System.out.println("falseingg");
  }

  @AfterSuite
  public void afterSuite() {
  }

}
