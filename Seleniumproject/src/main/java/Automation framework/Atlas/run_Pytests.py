import subprocess

def run_pytest_with_allure():
    try:
        # Step 1: Run pytest and generate allure results
        subprocess.run(["pytest", "--alluredir=allure-results"], check=True)

        # Step 2: Generate Allure report
        subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"], check=True)

        # Step 3: Serve Allure report in a browser
        subprocess.run(["allure", "serve", "allure-results"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_pytest_with_allure()