package com.testleaf.pages;

import org.openqa.selenium.By;

import com.testleaf.base.ProjectSpecificMethods;

public class HomePage extends ProjectSpecificMethods {

	public MyHomePage clickCRMSFA()
	{
		return new MyHomePage();
	}
    public LoginPage clickLogout()
    {
    	driver.findElement(By.className("decorativeSubmit")).click();
    	return new LoginPage();
    	
    }
    public HomePage verifyLoginSuccess()
    {
    	
    	return this;
    }
}
