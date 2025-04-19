package JavaAdvanceOOPS;

import java.time.Duration;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;

import io.github.bonigarcia.wdm.WebDriverManager;

public class Listprogram {
	public static void main(String[] args)
	{
		//Setup the chromedriver
		WebDriverManager.chromedriver().setup();
		
		//Open the browser  (chrome)
		ChromeDriver driver = new ChromeDriver();
		
	    //Implicit wait
		driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(30));
		
		//Maximize the window
		driver.manage().window().maximize();
		
		//findelement -> will return first matching web element !!!
		
		//find all the dropdown
	   List<WebElement> dropdown = driver.findElements(By.tagName("select"));
	   //find the count 
	   System.out.println(dropdown.size());
	   //select the first dropdown
	   WebElement firstDropDown = dropdown.get(2);
	   //choose
	   Select dd = new Select(firstDropDown);
	   dd.selectByIndex(2);
	}

}
