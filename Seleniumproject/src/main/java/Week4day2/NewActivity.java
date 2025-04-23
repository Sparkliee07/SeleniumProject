package Week4day2;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class NewActivity {
	public static void main(String[] args) throws InterruptedException
	{
	WebDriverManager.chromedriver().setup();
	ChromeDriver  driver = new ChromeDriver();
	driver.get("https://erail.in/");
	driver.manage().window().maximize();
	WebElement drom = driver.findElement(By.id("txtStationFrom"));
	
	drom.clear();
	drom.sendKeys("MS");
	Thread.sleep(400);
	drom.sendKeys(Keys.TAB);
     
	WebElement to = driver.findElement(By.id("txtStationTo"));
	to.clear();
	to.sendKeys("MDU");
	Thread.sleep(400);
	to.sendKeys(Keys.TAB);
	
	//deselect sorton date
	
	

}
}
