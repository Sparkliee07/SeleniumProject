package com.testleaf.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;

import com.testleaf.base.ProjectSpecificMethods;

public class LoginPage extends ProjectSpecificMethods{

	public LoginPage enterUserName()
	{
		WebElement eleUserName = driver.findElement(By.xpath("//input[@id='username']"));
		eleUserName.sendKeys("DemoSalesManager");
		return this;
	}
	public LoginPage enterPassword()
	{
		driver.findElement(By.id("password")).sendKeys("crmsfa");
		 return this;
	}
	public HomePage clickLogin()
	{
		driver.findElement(By.className("decorativeSubmit")).click();
		return new HomePage();
	}
	 

}
