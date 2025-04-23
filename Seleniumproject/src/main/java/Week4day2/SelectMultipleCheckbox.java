package Week4day2;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class SelectMultipleCheckbox {
	public static void main(String[] args)
	{
	
	WebDriverManager.chromedriver().setup();
	ChromeDriver  driver = new ChromeDriver();
	driver.get("https://leafteaps.com/opentaps/control/main");
	driver.manage().window().maximize();
	List <WebElement> options =  driver.findElements(By.xpath("/label[text()='Select all the below checkboxes ']/following-sibling::input"));
	for(WebElement weboptions:options)
	{
		weboptions.click();
	}
	}
}
