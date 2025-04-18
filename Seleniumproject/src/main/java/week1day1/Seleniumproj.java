package week1day1;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class Seleniumproj {
	public static void main(String[] args)
	{
		//setup chrome driver
	WebDriverManager.chromedriver().setup();
	//Open the browser 
	ChromeDriver driver = new ChromeDriver();
	
	driver.get("http://leaftaps.com/opentaps/control/main");
	driver.manage().window().maximize();
	
	//identify webelement
	WebElement element = driver.findElement(By.id("username"));
	element.sendKeys("DemoSalesManager");
	driver.findElement(By.id("password")).sendKeys("crmsfa");
	driver.findElement(By.className("decorativeSubmit")).click();
	driver.findElement(By.linkText("CRM/SFA")).click();
	driver.findElement(By.linkText("Leads")).click();
	driver.findElement(By.linkText("Create Lead")).click();
	driver.findElement(By.id("createLeadForm_companyName")).sendKeys("TestLead");
	driver.findElement(By.id("createLeadForm_firstName")).sendKeys("Haja");
	driver.findElement(By.id("createLeadForm_lastName")).sendKeys("J");
	driver.findElement(By.name("submitButton")).click();
	
	String Text = driver.findElement(By.id("viewLead_firstName_sp")).getText();
	System.out.println(Text);
	}
	
	

}
