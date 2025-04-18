package week1day1;

import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class LearnEdit {
	public static void main(String[] args) throws InterruptedException
	{
		WebDriverManager.chromedriver().setup();
		//Open the browser 
		ChromeDriver driver = new ChromeDriver();
		
		driver.get("http://www.leafground.com/pages/Edit.html");
		driver.manage().window().maximize();
		driver.findElement(By.id("email")).sendKeys("Haja");
		Thread.sleep(3000);
		driver.findElement(By.id("email")).clear();
		
		driver.findElement(By.id("email")).sendKeys("J");
	}

}
