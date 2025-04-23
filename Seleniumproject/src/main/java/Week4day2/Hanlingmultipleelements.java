package Week4day2;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class Hanlingmultipleelements {
	public static void main(String[] args)
	{
		WebDriverManager.chromedriver().setup();
		ChromeDriver  driver = new ChromeDriver();
		driver.get("https://leafteaps.com/opentaps/control/main");
		driver.manage().window().maximize();
		List <WebElement> inputs = driver.findElements(By.className("name"));
		for(int i=0;i<inputs.size();i++)
		{
			WebElement input = inputs.get(i);
			@SuppressWarnings("deprecation")
			String name = input.getAttribute("name");
			System.out.println(name);
		}
		
		
	}

}
