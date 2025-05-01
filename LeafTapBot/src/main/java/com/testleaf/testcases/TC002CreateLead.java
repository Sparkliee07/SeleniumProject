package com.testleaf.testcases;

import org.testng.annotations.Test;

import com.testleaf.pages.LoginPage;

public class TC002CreateLead {
	
	@Test
	public void runcreateLead()
	{
		new LoginPage()
		.enterUserName()
		.enterPassword()
		.clickLogin()
		.clickCRMSFA()
		.clickLeadsLink()
		.enterCompanyName();
	}

}
