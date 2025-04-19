package week1day1;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;

import io.github.bonigarcia.wdm.WebDriverManager;

public class LearnAlerts {
	public static void main(String[] args) throws InterruptedException
	{
		/*
		   Alert:
		A kind of notification  popup/dialog which provides some information
		1.Modal dialog
		
		a.) Simple alert ->   it has one button and a text message - accept(), getText()
		b.)prompt alert ->it hass 2 button and a input textfield -accept(),dismiss(),getText(),sendKeys()
		c.) confirmation alert -> it has 2 buttons and a text message accept(),dismiss(),getText(),
		
		Exceptions ; 
		1.Unhandled exception when you try to perfrom any actions without handling alert 
		2.NoAlertPresentException trying to handle when no alert is present 
		
		Characteristics of alert 
		 1.Cannot inspect the alert 
	     2. Cannot interact with main window unless alert is handled 
		 3. 
		2.Non modal dialog 
		--> sweet alert if user able to inspect the element is called sweet alert interacted as usual

		    */
		
		WebDriverManager.chromedriver().setup();
		ChromeDriver driver = new ChromeDriver();
		driver.get("https://www.leafground.com/pages/Alert.html");
		driver.manage().window().maximize();
		
		driver.findElement(By.xpath("//button[text()='Alert Box']")).click();
		Alert alert = driver.switchTo().alert();
		Thread.sleep(3000);
		System.out.println(alert.getText());
		alert.accept();
			
		//confirm box
        driver.findElement(By.xpath("//button[text()='Confirm Box']")).click();
		Alert alert1 = driver.switchTo().alert();
		Thread.sleep(3000);
		System.out.println(alert1.getText());
		alert1.dismiss();
		
		//prompt
		 driver.findElement(By.xpath("//button[text()='Prompt Box']")).click();
			Alert alert2 = driver.switchTo().alert();
			alert2.sendKeys("ABC");
			Thread.sleep(3000);
			System.out.println(alert2.getText());
			alert2.dismiss();
	}

}
