package week1day1;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class FrameClassroom {
 public static void main(String[] args)
 {
	 WebDriverManager.chromedriver().setup();
     ChromeDriver driver = new ChromeDriver();
     driver.get("https//www.leafground.com/pages/frame.html");
   driver.manage().window().maximize();
  driver.switchTo().frame("iframe");
  driver.findElement(By.xpath("//button[text()=Try it")).click();
  Alert alert = driver.switchTo().alert();
  alert.sendKeys("Haja");
  alert.accept();
  String text= driver.findElement( By.id("demo")).getText();
  if(text.contains("Haja"))
  {
	  System.out.print("Success");
	  
  }
  else
  {
	  System.out.println("Failed");
  }
  
  
 }

}
