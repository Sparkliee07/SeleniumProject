package Week4day2;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class DoubleClick {
	public static void main(String[] args)
	{
		//setup chrome driver
	WebDriverManager.chromedriver().setup();
	ChromeOptions options = new ChromeOptions();
	options.addArguments("disable notifications");
	//Open the browser 
	ChromeDriver driver = new ChromeDriver();
	
	driver.get("http://www.myntra.com");
	driver.manage().window().maximize();
	WebElement men = driver.findElement(By.xpath("//a[text()='Men']"));
	//create a object for actios class 
	Actions builder = new Actions(driver);
	//Double click on men we need to put perform
	//builder.doubleClick(men).perform();
	
	//no exceptions for action class
	//mouseover on men
	builder.moveToElement(men).perform();
	
	//drag and drop 
	

	
	
	
}
}