package com.testleaf.testcases;

import org.testng.annotations.Test;

import com.testleaf.base.ProjectSpecificMethods;
import com.testleaf.pages.LoginPage;

public class TC001Login extends ProjectSpecificMethods {
	
	@Test
	public void runLoginTest()
	{
		
		new LoginPage().enterUserName()
		.enterPassword()
		.clickLogin()
		.clickLogout();
		
	}

}
