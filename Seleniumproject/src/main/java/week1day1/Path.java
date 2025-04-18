package week1day1;

import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class Path {
	public static void main(String[] args) throws InterruptedException
	{
	
	WebDriverManager.chromedriver().setup();
	//Open the browser 
	ChromeDriver driver = new ChromeDriver();
	
	driver.get("http://www.leafground.com/pages/Edit.html");
	driver.manage().window().maximize();
}

}