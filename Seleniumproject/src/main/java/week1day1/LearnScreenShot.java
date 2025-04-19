package week1day1;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class LearnScreenShot {
	public static void main(String[] args) throws IOException
	{
	WebDriverManager.chromedriver().setup();
	ChromeOptions options = new ChromeOptions();
    options.addArguments("--disable-notifications");
	//Open the browser 
	ChromeDriver driver = new ChromeDriver(options);
     driver.get("https://www.irctc.co.in/nget/train-search");
     driver.manage().window().maximize();
	
	
	File source = driver.getScreenshotAs(OutputType.FILE);
 File destination = new File("./screenshot.png");
 FileUtils.copyFile(source, destination);
}
}