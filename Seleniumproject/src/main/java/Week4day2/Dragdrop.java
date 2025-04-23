package Week4day2;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class Dragdrop {
	public static void main(String[] args)
	{
		
	WebDriverManager.chromedriver().setup();
	ChromeOptions options = new ChromeOptions();
	options.addArguments("disable notifications");
	//Open the browser 
	ChromeDriver driver = new ChromeDriver();
	
	driver.get("http://www.leafground.com/pages/drag.html");
	driver.manage().window().maximize();

	WebElement dragele = driver.findElement(By.id("draggable"));
	WebElement dropele = driver.findElement(By.id("droppable"));
	Actions builder = new Actions(driver);
	builder.dragAndDrop(dragele, dropele).perform();
	
	int x = dropele.getLocation().getX();
	int y = dropele.getLocation().getY();
	builder.dragAndDropBy(dropele, x, y).perform();
	builder.clickAndHold(dragele)
	.moveToElement(dropele) //hover on element 
	.release()
	.perform();
	
	//Rightclick
	builder.contextClick(dragele).perform();
	
	/* Learn sortable
	 * WebDriverManager.chromedriver().setup();
	ChromeOptions options = new ChromeOptions();
	options.addArguments("disable notifications");
	//Open the browser 
	ChromeDriver driver = new ChromeDriver();
	
	driver.get("http://www.leafground.com/pages/drag.html");
	driver.manage().window().maximize();

	WebElement dragele = driver.findElement(By.xpath("li[text()='drag']"));
	WebElement dropele = driver.findElement(By.id("li[text()='droppable']"));
	Actions = new Actions(driver);
	builder.dragAndDropBy(item2.item5.getLocatio().getX(),item5
	*/
	
/*control click
	
	WebElement item1 = driver.findElement(By.xpath("li[text()='item1']"));
	WebElement item2 = driver.findElement(By.id("li[text()='item2']"));
	WebElement item3 = driver.findElement(By.id("li[text()='item3']"));
	WebElement item4 = driver.findElement(By.id("li[text()='item4']"));
	WebElement item5 = driver.findElement(By.id("li[text()='item5']"));
	*/
}
}
