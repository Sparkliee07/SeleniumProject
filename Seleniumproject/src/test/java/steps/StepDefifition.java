package steps;

@CucumberOptions(feautres="src/test/java/feautres/Login.feautre",
                 glue = "steps",
                 monochrome = true)
//features =""  path for the giveb proj
//glue = it will bind the data 
//monochrome = true  it will remove the junk character
publish = true will generate cucumber report

public class StepDefifition extends AbstractTestNGCucumberTests {

	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
 
	}

}
