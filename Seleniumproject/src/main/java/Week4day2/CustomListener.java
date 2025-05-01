package Week4day2;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;

public class CustomListener implements IRetryAnalyzer {

	
	int count =0;
	public boolean retry(ITestResult result) {
		// TODO Auto-generated method stub
		if(count<1)
		{
			count++:
			return true;
		}
		return false;
	}
	

}
