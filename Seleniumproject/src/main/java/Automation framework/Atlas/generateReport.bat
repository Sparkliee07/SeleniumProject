:: # Run behave tests with Allure formatter
behave -f allure_behave.formatter:AllureFormatter -o ../../Reports/allure-results

pytest --alluredir=../../Reports/allure-results

:: # Generate Allure report from the test results
allure generate reports/allure-results -o ../../Reports/allure-report --clean
