package week1day1;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class LearnFrame {
	
	public static void main(String[] args)
	
	{
		/*
		Frame 
		In frame tag id or name is always same
		it means html structure another srtuctuew 
		Frame is like a ad page for web element 
		tag name will be frame/iframe
		*/

		  
		      WebDriverManager.chromedriver().setup();
		      ChromeDriver driver = new ChromeDriver();
		      driver.get("https//www.leafground.com/pages/frame.html");
		    driver.manage().window().maximize();
		   driver.switchTo().frame(0);
		 //name or id
		//webElement
		  driver.findElement(By.id("click")).click();
		  // to get out of frame
		  driver.switchTo().defaultContent();
		String text = driver.findElement(By.tagName("h1")).getText();
		System.out.println(text);
		WebElement frameEle = driver.findElement(By.xpath("(//div[@id='wrapframe']/iframe[2]"));
		 driver.switchTo().frame(frameEle);
		  driver.switchTo().frame("frame2");
		 driver.findElement(By.id("click1")).click();
		//one level back 
		 driver.switchTo().parentFrame();
		 

	}

}
